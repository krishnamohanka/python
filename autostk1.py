from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from time import time
import datetime

driver = webdriver.Chrome(r"C:\Users\krsna\Downloads\chromedriver_win32\chromedriver.exe")

driver.get("https://kite3.zerodha.com/")

usrInput=driver.find_elements_by_tag_name("input")[0]
pwdInput=driver.find_elements_by_tag_name("input")[1]

usrInput.send_keys("YK8879")
sleep(1)
pwdInput.send_keys("kitch123")
sleep(1)
driver.find_element_by_tag_name("button").click()

delay = 30#seconds
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
sleep(1)
driver.find_element_by_tag_name("button").click()

try:
    #myElem = WebDriverWait(driver, delay).until(EC.text_to_be_present_in_element((By.CLASS_NAME,'nickname'),'Konathalvalap'))
    myElem1 = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='vddl-list list-flat']")))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

mrketwatchlist = driver.find_element_by_xpath("//div[@class='vddl-list list-flat']")
element_to_hover_over = None

t_end = time() + 15 * 1

dt = datetime.datetime.fromtimestamp(int(time())).strftime('_%Y_%m_%d')
filname = "BhartiAirtel" + dt
#while(time() < t_end):
while(1):
    for index,itm in enumerate(mrketwatchlist.find_elements_by_class_name("info")):
        if(index==0):
            with open(filname, "a+") as f:
                print (itm.text)
                name = itm.text.split('\n')[0]
                if(str(itm.text).find("\n")>-1):
                    ltp = itm.text.split('\n')[1].split('%')[1]
                    print (ltp+","+str(time()))
                    f.write(ltp+","+str(time())+"\n")
                    element_to_hover_over = itm


# hover = ActionChains(driver).move_to_element(element_to_hover_over)
# hover.perform()
#
# sleep(1)
#
# hoverBtns =  driver.find_elements_by_xpath("//span/button")
#
# buybtn = hoverBtns[0]
#
# sellbtn = hoverBtns[1]
#
# buybtn.click()
#
#
# try:
#     buywin = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.CLASS_NAME,"order-window-cover buy variety-regular")))
#     print ("Page is ready!")
# except TimeoutException:
#     print ("Loading took too much time!")
#
#     buywin = driver.find_element_by_class_name("order-window-cover buy variety-regular")
#
#     buyInputs = buywin.find_elements_by_tag_name("input")
#
#     misRadio = [m for m in buyInputs if m.get_attribute('label')== 'MIS'][0]
#
#     misRadio.click()
