from hashlib import new
from operator import ne
import os
import sys
from telnetlib import EC
from turtle import title
#from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from selenium.webdriver.chrome.service import Service
import random
from webdriver_manager.chrome import ChromeDriverManager
#import tzlocal
import logging
count_error=0
'''def wait_scheduler():
    scheduler = BlockingScheduler()
    scheduler = BlockingScheduler(timezone='Asia/Taipei')
    #scheduler.add_job(for_scheduler, 'cron', day_of_week='*',hour='0-23',minute='55')
    #scheduler.add_job(job, 'cron', day_of_week='mon-sun', hour=6, minute=31)
    scheduler.add_job(for_scheduler,'interval', minutes=1)
    print('執行異常   30分後再重新執行....')
    scheduler.start()

def do_scheduler():
    scheduler = BlockingScheduler()
    scheduler = BlockingScheduler(timezone='Asia/Taipei')
    scheduler.add_job(for_scheduler, 'cron', day_of_week='*',hour='8',minute=str(random.randint(1,10)))
    #scheduler.add_job(job, 'cron', day_of_week='mon-sun', hour=6, minute=31)
    #scheduler.add_job(for_scheduler,'interval', minutes=30)
    print('執行完畢 將於每日8時自動填寫')
    scheduler.start()
'''

def job(num):
    count_overtime=0
    account = contents[num]
    password = contents[num+1]
    print('你的帳號:',account)
    print('你的密碼:',password)
    #設定WebDriver參數       
    options1=webdriver.ChromeOptions()
    #options1.add_experimental_option('excludeSwitches',['enable-automation','enable-logging'])
    options1.add_experimental_option('excludeSwitches',['enable-automation'])
    options1.add_argument("--start-maximized")# 設定瀏覽器大小
    options1.add_argument('log-level=3')      #INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
    #options1.add_argument('--headless')  #無頭模式
    options1.add_argument('--disable-gpu')  
    #自動安裝webdriver
    service1=Service(ChromeDriverManager().install())   
    while count_overtime<4:
        try:
            driver=webdriver.Chrome(service=service1 ,options=options1)
            driver.get(url)
            driver.set_page_load_timeout(10)
            driver.implicitly_wait(10)            
            # 定位日期輸入欄位, 並輸入日期
            element1 = driver.find_element(By.ID, 'txtAccount')
            element1.send_keys(account)
            element2 = driver.find_element(By.ID, 'txtPwd')
            element2.send_keys(password)
            # 定位選單所在欄位並點擊
            element3 = driver.find_element(By.ID, 'btnSubmit')
            try:
                WebDriverWait(driver,5,1).until(EC,title_is('員工體溫量測暨生活軌跡紀錄表'))
            except:
                break
            finally:
                element3.click()
                element4 = driver.find_element(By.ID, '[1].DailyTemperature1')
                #element4.send_keys('\ue003')
                element4.clear()
                element4.send_keys(random.uniform(36.1, 37.0))
                element5 = driver.find_element(By.ID, 'IamFine')
                if element5.get_attribute("checked") != "true":
                    element5.click()
                else:
                    print(datetime.now().strftime('%Y-%m-%d %H:%M'),'今日已填寫過')
                    print('-----------------------------------------------------')
                    driver.close()
                    break
                element6 = driver.find_element(By.ID, 'search')
                element6.click()
                alert1= driver.switch_to.alert
                alert1.accept()
                alert2= driver.switch_to.alert
                alert2.accept()            
                print(datetime.now().strftime('%Y-%m-%d %H:%M'),'已填寫ok')
                print('-----------------------------------------------------')
        except:            
            if count_overtime==3:
                print(datetime.now().strftime('%Y-%m-%d %H:%M'),'填寫失敗')
                print('-----------------------------------------------------')
                count_overtime=count_overtime+1
                global count_error
                count_error+=1
                break
            else:
                print('等候逾時  重新填寫中...')
                driver.close()
                count_overtime=count_overtime+1
                continue
        finally:
            driver.quit()  # 關閉瀏覽器, 結束 webdriver process
            
def for_scheduler():
    forcount(count_len)

def forcount(count):
    scheduler = BlockingScheduler()
    scheduler = BlockingScheduler(timezone='Asia/Taipei')
    for i in range(count):
        print('第',i+1,'組')
        if i==0:
            job(i)
        else:
            job(i*2)
    global count_error    
    if count_error>0:
        scheduler.remove_all_jobs
        scheduler.add_job(for_scheduler,'interval', minutes=30)
        print('有帳號執行異常 30分後再重新執行....')
        scheduler.start()
    else:
        scheduler.remove_all_jobs
        scheduler.add_job(for_scheduler, 'cron', day_of_week='*',hour='8',minute=str(random.randint(1,10)))
        #scheduler.add_job(for_scheduler,'interval', minutes=30)
        print('執行完畢 將於每日8時1~10分自動填寫')
        scheduler.start()


if __name__ == '__main__':
    print("Current version of Python is ", sys.version)
    print('Start!! 每日填體溫v20220709')
    #以下設定webdriver參數
    #隱藏webdriver mannager 訊息
    logging.getLogger('WDM').setLevel(logging.ERROR) 
    logging.getLogger('apscheduler').setLevel(logging.ERROR) 
    print('Login https://hicgate.honghwa.com.tw/COVID-19_Daily has been started!')
    print('Read auth.txt...')
    auth_path = './auth.txt'
    url = 'https://hicgate.honghwa.com.tw/COVID-19_Daily/'
    if os.path.isfile('./auth.txt') is False:
        print('%s file is not found!' % auth_path)
        input("Please press the Enter key to quit")
        sys.exit(1)      
    else:
        print('Read auth is done')       
    infopen = open(auth_path, 'r',encoding="utf-8")
    outfopen = open('./b.txt', 'w',encoding="utf-8")
    lines = infopen.read().splitlines()
    for line in lines:
        line = line.strip()
        if len(line)!=0:
            outfopen.writelines(line)
            outfopen.write('\n')      
    infopen.close()
    outfopen.close()
    os.remove('./auth.txt')
    os.rename('./b.txt','./auth.txt')    
    auth_handler = open(auth_path, 'r')
    contents = auth_handler.read().splitlines()
    print('密碼本:',contents)
    print('-----------------------------------------------------')
    if len(contents)%2==1 or len(contents)==0:
        print('auth.txt should have account and password!')
        input("Please press the Enter key to quit")
        sys.exit(1)
    auth_handler.close()
    count_len=int(len(contents)/2) #計算幾組帳密
    for_scheduler() 
