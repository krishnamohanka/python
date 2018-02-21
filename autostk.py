from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
driver = webdriver.Chrome(r"C:\Users\NG6EADA\Downloads\chromedriver_win32\chromedriver.exe")

# while(1):
#     driver.get("https://www.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm")
#     trs = driver.find_elements_by_xpath("//tr")
#     for tr in trs:
#         tds = tr.find_elements_by_tag_name("td")
#         try:
#             print tds[0].text+" "+tds[6].text
#         except:
#             pass
#     sleep(5)

driver.get("http://www.moneycontrol.com/terminal/index_v1.php?index=31")
trs= driver.find_elements_by_xpath("//div[3]/table/tbody/tr")
tds=trs[0].find_elements_by_tag_name("td")

prevValue = 0
while(1):
    name= tds[0].text
    value= tds[1].text

    if(not value == prevValue ):
        print value
        prevValue = value;
    sleep(1)



#print (elem)
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
driver.close()
