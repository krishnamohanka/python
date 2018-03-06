from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
driver = webdriver.Chrome(r"C:\Users\krsna\Downloads\chromedriver_win32\chromedriver.exe")

driver.get("https://kite3.zerodha.com/")

usrInput=driver.find_elements_by_tag_name("input")[0]
pwdInput=driver.find_elements_by_tag_name("input")[1]

usrInput.send_keys("YK8879")
sleep(1)
pwdInput.send_keys("")
driver.find_element_by_tag_name("button").click()

delay = 15#seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element((By.TAG_NAME,'h2'),'Security questions'))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

qdict ={"car":"","vegetable":"","birthplace":"","email":""}

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
sleep(1)
driver.find_element_by_tag_name("button").click()

try:
    myElem = WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element((By.CLASS_NAME,'nickname'),'Konathalvalap'))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

mrketwatchlist = driver.find_element_by_xpath("//div[@class='vddl-list list-flat']")


while(1):
    for itm in mrketwatchlist.find_elements_by_class_name("info"):
        name = itm.text.split('\n')[0]
        ltp = itm.text.split('\n')[1].split('%')[1]
        print (name + ", "+ltp)
        sleep(2)
