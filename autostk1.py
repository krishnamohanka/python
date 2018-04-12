from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os
import datetime
options = webdriver.ChromeOptions()
#options.add_argument('headless')

driver = webdriver.Chrome(r"C:\Users\NG6EADA\Downloads\chromedriver_win32\chromedriver.exe",options=options)
driver.maximize_window()
driver.get("https://kite3.zerodha.com/")

usrInput=driver.find_elements_by_tag_name("input")[0]
pwdInput=driver.find_elements_by_tag_name("input")[1]

usrInput.send_keys("YK8879")
time.sleep(1)
pwdInput.send_keys("kitch123")
driver.find_element_by_tag_name("button").click()

delay = 15#seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element((By.TAG_NAME,'h2'),'Security questions'))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

qdict ={"car":"blue","vegetable":"onion","birthplace":"kalpetta","email":"yahoo"}

q1=driver.find_elements_by_tag_name("label")[0]
q2=driver.find_elements_by_tag_name("label")[1]

a1=""
a2=""
for k in qdict.keys():
    if str(q1.text).find(k)>1:
        a1=qdict[k]
        break
    else:
        a1="yellow"

for k in qdict.keys():
    if str(q2.text).find(k)>1:
        a2=qdict[k]
        break
    else:
        a2="yellow"

driver.find_elements_by_tag_name("input")[0].send_keys(a1)
driver.find_elements_by_tag_name("input")[1].send_keys(a2)
time.sleep(1)
driver.find_element_by_tag_name("button").click()

try:
    myElem = WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element((By.CLASS_NAME,'nickname'),'Konathalvalap'))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

time.sleep(10)
mrketwatchlist = driver.find_element_by_xpath("//div[@class='vddl-list list-flat']")

dt = datetime.datetime.fromtimestamp(int(time.time())).strftime('_%Y_%m_%d')
filname = "21STocks_" + dt+".csv"

with open(filname, "a+") as f:
    for index, itm in enumerate(mrketwatchlist.find_elements_by_class_name("info")):
        print (itm.text)
        name = itm.text.split('\n')[0]
        f.write(name + ",")
    f.write("TIME "+"\n")


while(1):
    ltp_writer = ""
    with open(filname, "a+") as f:
        for index,itm in enumerate(mrketwatchlist.find_elements_by_class_name("info")):
            print (itm.text)
            #name = itm.text.split('\n')[0]
            if(str(itm.text).find("\n")>-1):
                ltp = itm.text.split('\n')[1].split('%')[1]
                ltp_writer = ltp_writer + ltp + ","
                #print (ltp+","+str(time.time()))
                #f.write(ltp+","+str(time.time())+"\n")

        ltp_writer=ltp_writer+str(time.time())+"\n"
        f.write(ltp_writer)

                    #element_to_hover_over = itm
driver.close()
