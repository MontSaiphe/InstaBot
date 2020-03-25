from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random 
import sys
import re
import datetime


class  InstagramBot :

    def __init__(self , username , password , Fol, itterations , statsName) :
        self.username = username
        self.password = password
        self.statsName = statsName
        #self.driver = webdriver.Firefox()
        self.stats = [[0,0,0,0,0,0,0,0]]*(itterations+2)
        self.StatsNb = 0
        self.FolNb = Fol
        self.itterations = itterations
   
    def StopBot(self) :
        self.UpdateStats()
        sys.exit()

    def login(self):
        self.driver = webdriver.Firefox()
        driver = self.driver
        driver.get("https://www.instagram.com/")
        usernameBx =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME,"username")))
        passwordBx = driver.find_element_by_name("password")
        usernameBx.send_keys(self.username)
        time.sleep(.5)
        passwordBx.send_keys(self.password ,Keys.RETURN )
        time.sleep(3)
        later = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//button[text()="Plus tard"]')))
        later.click()
        #self.UpdateStats()
        self.StatsNb += 1


    def accounts(self , accounts):
        time.sleep(2)
        driver = self.driver   
        account = accounts  
        last_post_liked = [[""]* (len(account))] *3
        while(True):                   
            for a in range (0 , 4):
                for i in range (len(accounts)) : 
                    if(self.itterations == 0):
                        break
                    driver.get("https://www.instagram.com/"+account[i])
                    time.sleep(3)
                    if(len(driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/div")) == 2):
                        picture =  driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]")
                    else:
                        picture =  driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]")
                    picture.click()
                    for b in range (a):
                        next = driver.find_element_by_xpath('//a[text()="Suivant"]')
                        next.click()
                    time.sleep(2)
                    if(driver.current_url != last_post_liked[a][i]):
                        last_post_liked[a][i] = driver.current_url
                        if(self.CheckFollowerNb() > self.FolNb+10):                          
                            self.Fol()
                            self.itterations -=1
                            self.UpdateStats()
                            # driver.close()
                            #time.sleep(10)   
                            time.sleep(1200 + random.randint(100 , 400))  
                            #time.sleep(3600 + random.randint(300 , 1200))  
                            #self.login()
        self.StopBot()

    def CheckFollowerNb(self):
        
        driver = self.driver  
        time.sleep(3)         
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button")))
        like = self.GetLikeBt()     
        likeTxt = like.text
        if(likeTxt[0] == 'a'):
            return 1
        likeNb = int((re.findall('\d+' , likeTxt))[0])
        if(likeNb < self.FolNb -10 or likeNb < 11):
            return 1
        else:
            like.click()   
            bug = self.CheckForElement("/html/body/div[5]/div/div[2]/div/div/div[1]/div[3]" , By.XPATH )
            if(bug == False ):
                sys.exit()

            lastAc = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/div[10]")
            driver.execute_script('arguments[0].scrollIntoView()' , lastAc)
            scroll = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div")      
            lastHt , Ht = 0 , 1
            scrolled = 0
            while lastHt != Ht : 
                lastHt = Ht
                Ht = driver.execute_script("""arguments[0].scrollBy(0, 500); return arguments[0].scrollHeight; """ , scroll)
                scrolled +=500
                time.sleep(1.5)
            driver.execute_script("""arguments[0].scrollBy(0, -100);""" , scroll)
            time.sleep(1)
            driver.execute_script("""arguments[0].scrollBy(0, 200);""" , scroll)
            scrolled +=100      
            lastHt , Ht = 0 , 1
            while lastHt != Ht : 
                lastHt = Ht
                Ht = driver.execute_script("""arguments[0].scrollBy(0, 500); return arguments[0].scrollHeight; """ , scroll)
                scrolled +=500 
                time.sleep(.75)
            
            toFollow = 0
            for i in range (11, 0 , -1):
                followTxt = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/div["+str(i)+"]/div[3]/button").text
                if(followTxt == "S’abonner"):
                    toFollow +=1
            time.sleep(.75)
            for i in range(likeNb -11 , 0 , -1):
                driver.execute_script("""arguments[0].scrollBy(0, -60);""" , scroll)
                time.sleep(.1)
                followTxt = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/div[1]/div[3]/button").text
                if(followTxt == "S’abonner"):
                    toFollow +=1
            driver.execute_script("arguments[0].scrollBy(0," + str(scrolled) + "-40);" , scroll)

            #follows = driver.find_elements(By.XPATH , '//button[text()="S’abonner"]')
            #follows = scroll.find_elements_by_xpath('//button[text()="Plus tard"]') 

            return toFollow

            #FolNb = self.FolNb
            #print (len(driver.find_elements_by_xpath("/html/body/div[5]/div/div[2]/div/div/div")))
            

    def Fol(self):
        FolNb = self.FolNb
        driver = self.driver  
        scroll = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div")      
        driver.execute_script("""arguments[0].scrollTo(0, 0) """ , scroll)
        time.sleep(3)
        for i in range(1,7):
            if(FolNb != 0):
                follow = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/div["+str(i)+"]/div[3]")
                followTxt = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/div["+str(i)+"]/div[3]/button").text
                if(followTxt == "S’abonner"):
                    follow.click()  
                    time.sleep( 2+ random.random() +  random.random() +  random.random())                
                    followTxt = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/div["+str(i)+"]/div[3]/button").text             
                    FolNb -=1
                    block = self.CheckForElement('//button[text()="Signaler un problème"]' , By.XPATH)
                    if(block == True):
                        print("followBlock") 
                        self.StopBot          
        driver.execute_script("""arguments[0].scrollBy(0, 420);""" , scroll)   
        while(FolNb > 0):
            driver.execute_script("""arguments[0].scrollBy(0, 60);""" , scroll)   
            time.sleep(1)      
            follow = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/div[7]/div[3]")
            followTxt = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/div[7]/div[3]/button").text
            if(followTxt == "S’abonner"):
                follow.click()  
                time.sleep(2 + random.random() +  random.random() +  random.random())                 
                followTxt = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div/div[10]/div[3]/button").text             
                FolNb -=1
                block = self.CheckForElement('//button[text()="Signaler un problème"]' , By.XPATH)
                if(block == True):
                    print("followBlock") 
                    self.StopBot  




    def UpdateStats(self):
        driver = self.driver
        statNb = self.StatsNb
        driver.get("https://www.instagram.com/" + self.username)
        followers = driver.find_element_by_xpath('//a[@href="/'+self.username+'/followers/"]/span')
        followersNb = int(followers.text)
        following = driver.find_element_by_xpath('//a[@href="/'+self.username+'/following/"]/span')
        followingNb = int(following.text)

        self.stats[statNb][0] = datetime.date.today().strftime("%d/%m/%Y")
        self.stats[statNb][1] = time.strftime("%H:%M:%S",time.localtime())
        self.stats[statNb][2] =followersNb 
        self.stats[statNb][3] =followingNb 
        self.stats[statNb][4] =self.FolNb 

        time.sleep(3)
        pic =  driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]" )
        pic.click()
        for i in range (1 , 4):
            time.sleep(3)
            like = self.GetLikeBt()
            likeNb=like.text
            #like.click()
            #time.sleep(2)
            #driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div/div[2]/button").click()
            #time.sleep(2)
            if (likeNb[0] != 'a'):
                self.stats[statNb][i+4] = int((re.findall('\d+' , likeNb))[0])
            else:
                self.stats[statNb][i+4] = 0
            

            next = driver.find_element_by_xpath('//a[text()="Suivant"]')
            next.click()      
        print(self.stats[statNb])
        self.StatsNb += 1
        textFile = open(self.statsName + "Stats" , "a")
        statsStr = ""
        for s in self.stats[statNb]:
            statsStr += "|" + str(s) + "|"
        textFile.write(statsStr + "\n")
        textFile.close()


    def CheckForElement(self, attribute, by ):
        driver = self.driver
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, attribute)))
            return True
        except:       
            return False


    def GetLikeBt(self):
        driver = self.driver
        like = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button")
        likeTxt = like.text
        if(likeTxt == ''):
            like = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button")
        return like
    
    def accTest(self , accounts):
        driver = self.driver
        account = accounts  
        for i in range (len(accounts)) : 
            driver.get("https://www.instagram.com/"+account[i])
            time.sleep(2)
        sys.exit()





#accs = [ "maths_memes_" , "science24hour" , "algebruhhh.memes" , "iota_academy__" , "mathsloverashish" , "mr.mathematicians"]
accs = ["coding_stuff" , "innovative.brands" , "_programmerhumor_" ] #, "nerds_coding" , "allgeeklife" , "life.ofacoder"]
#time.sleep(3600)
time.sleep(1300)
IG = InstagramBot("programmer.laughs" , "doudou99" ,5 , 10 ,"prog")
IG.login()
#IG.driver.close()
#IG.login()
IG.UpdateStats()
IG.accounts(accs)
#IG.UpdateStats()
#IG.accTest(accs)
#IG.accounts(accs)


#v1Nh3 kIKUG  _bz0w
#/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a

