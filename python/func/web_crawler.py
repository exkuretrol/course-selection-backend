import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import schedule
import time

# https://www.mcu.edu.tw/student/new-query/sel-query/index.html 選課首頁
def General_Education(semester,lst):   # 通識
    option = Options()
    option.add_argument('--headless')  # 啟動Headless 無頭
    option.add_argument('--disable-gpu') #關閉GPU 避免某些系統或是網頁出錯
    driver = webdriver.Chrome('/D:/大四(上)/專研/成品/爬蟲/chromedriver.exe',options = option)   # 執行chrome driver
    driver.get('https://www.mcu.edu.tw/student/new-query/sel-query/query_menu.asp?gdb=2&gyy=111')   # 連結網站(選擇學期)

    if semester == '1':
        driver.find_element(By.LINK_TEXT, '111學年度第1學期').click()
    elif semester == '2':
        driver.find_element(By.LINK_TEXT, '111學年度第2學期').click()
    driver.get('https://www.mcu.edu.tw/student/new-query/sel-query/query_4_up.asp')   # 連結網站(通識)
    
    # lst = []  # 存表格內容用
    campus = ['1', '2', '3', '4', '5', '6']
    for i in campus:
        # time.sleep(3)
        element2_campus = Select(driver.find_element(By.NAME, 'sch'))   # 抓校區選單的位置
        element2_campus.select_by_value(i)   # 選擇要找的校區 1~6->分別對應為北、桃、金、連、基、美
        driver.find_element(By.CSS_SELECTOR, 'body>form>table>tbody>tr:nth-child(2)>td:nth-child(3)>input[type=submit]:nth-child(1)').click()
        # 進入網頁
        driver.switch_to.window(driver.window_handles[1])   # 切換到視窗2
        
        try:
            table = driver.find_element(By.TAG_NAME, 'tbody')  # 抓表格位置
            # 抓表格内容
            tr_tags = table.find_elements(By.TAG_NAME, 'tr')  # 抓tr
            tr_tags = table.find_elements(By.TAG_NAME, 'tr')[1:]
            for tr in tr_tags:
                td_tags = tr.find_elements(By.TAG_NAME, 'td')  # 抓td
                for td in td_tags[:13]: #只提取前13列(不抓說明)
                    lst.append(td.text)
        except Exception as msg:
            print(msg)

        driver.switch_to.window(driver.window_handles[0])   # 回到視窗1

    driver.quit()
    return lst    # 回傳課表
'''-----------------------------------------------------'''
def Elective(semester,lst):   # 選修
    option = Options()
    option.add_argument('--headless')  # 啟動Headless 無頭
    option.add_argument('--disable-gpu') #關閉GPU 避免某些系統或是網頁出錯
    driver = webdriver.Chrome('/D:/大四(上)/專研/成品/爬蟲/chromedriver.exe',options = option)   # 執行chrome driver
    driver.get('https://www.mcu.edu.tw/student/new-query/sel-query/query_menu.asp?gdb=2&gyy=111')   # 連結網站(選擇學期)

    if semester == '1':
        driver.find_element(By.LINK_TEXT, '111學年度第1學期').click()
    elif semester == '2':
        driver.find_element(By.LINK_TEXT, '111學年度第2學期').click()
    driver.get('https://www.mcu.edu.tw/student/new-query/sel-query/query_3_up.asp')   # 連結網站(選修)
    
    # lst = []  # 存表格內容用
    ge = ['1', '2', '3', '4', '5']
    dt = ['02','03','04','05','08','09','11','13','14','16','17','18','19','21','22','23','24','25','26','27','31','32'
          ,'33','36','37','38','39','40','41','42','43','44','45','46','47','48','50','52','54','56','57','59'
          ,'65','67','68','70','82','83','88','89','90','91']
    for i in dt:
        for j in ge:
            # time.sleep(3)
            element1_department = Select(driver.find_element(By.NAME, 'dept'))   # 抓系的選單位置
            element1_department.select_by_value(i)   # 選擇要找的系 給系的號碼
            element1_grade = Select(driver.find_element(By.NAME, 'yr'))   # 抓年級選單的位置
            element1_grade.select_by_value(j)   # 選擇要找的年級 1~5
            driver.find_element(By.CSS_SELECTOR, 'body>form>table>tbody>tr:nth-child(2)>td:nth-child(4)>input[type=submit]:nth-child(1)').click()
            # 進入網頁
            driver.switch_to.window(driver.window_handles[1])   # 切換到視窗2
            
            try:
                table = driver.find_element(By.TAG_NAME, 'tbody')  # 抓表格位置
                # 抓表格内容
                tr_tags = table.find_elements(By.TAG_NAME, 'tr')  # 抓tr
                tr_tags = table.find_elements(By.TAG_NAME, 'tr')[1:]
                for tr in tr_tags:
                    td_tags = tr.find_elements(By.TAG_NAME, 'td')  # 抓td
                    for td in td_tags[:13]: #只提取前13列(不抓說明)
                        lst.append(td.text)
            except Exception as msg:
                print(msg)

            driver.switch_to.window(driver.window_handles[0])   # 回到視窗1

    driver.quit()
    return lst    # 回傳課表
'''-----------------------------------------------------'''
def Compulsory(semester):   # 必修
    option = Options()
    option.add_argument('--headless')  # 啟動Headless 無頭
    option.add_argument('--disable-gpu') #關閉GPU 避免某些系統或是網頁出錯
    driver = webdriver.Chrome('/D:/大四(上)/專研/成品/爬蟲/chromedriver.exe',options = option)   # 執行chrome driver
    driver.get('https://www.mcu.edu.tw/student/new-query/sel-query/query_menu.asp?gdb=2&gyy=111')   # 連結網站(選擇學期)

    if semester == '1':
        driver.find_element(By.LINK_TEXT, '111學年度第1學期').click()
    elif semester == '2':
        driver.find_element(By.LINK_TEXT, '111學年度第2學期').click()
    driver.get('https://www.mcu.edu.tw/student/new-query/sel-query/query_2_up.asp')   # 連結網站(必修)

    lst = []  # 存表格內容用
    ge = ['1', '2', '3', '4', '5']
    dt = ['01','02','04','05','08','09','11','13','14','16','17','18','19','21','22','23','24','25','26','27','28','30'
          ,'31','32','33','36','37','38','39','40','41','42','43','44','45','46','47','48','50','52','54','56','57','59'
          ,'65','67','68','70','80','81','82','83','88','89','90','91','96','99']
    for i in dt:
        for j in ge:
            # time.sleep(3)
            element1_department = Select(driver.find_element(By.NAME, 'dept'))   # 抓系的選單位置
            element1_department.select_by_value(i)   # 選擇要找的系 給系的號碼
            element1_grade = Select(driver.find_element(By.NAME, 'yr'))   # 抓年級選單的位置
            element1_grade.select_by_value(j)   # 選擇要找的年級 1~5
            driver.find_element(By.CSS_SELECTOR, 'body>form>table>tbody>tr:nth-child(2)>td:nth-child(4)>input[type=submit]:nth-child(1)').click()
            # 進入網頁
            driver.switch_to.window(driver.window_handles[1])   # 切換到視窗2
            
            try:
                table = driver.find_element(By.TAG_NAME, 'tbody')  # 抓表格位置
                # 抓表格内容
                tr_tags = table.find_elements(By.TAG_NAME, 'tr')  # 抓tr
                if i != '01':   # 不重複印title
                    tr_tags = table.find_elements(By.TAG_NAME, 'tr')[1:]
                for tr in tr_tags:
                    td_tags = tr.find_elements(By.TAG_NAME, 'td')  # 抓td
                    for td in td_tags[:13]: #只提取前13列(不抓說明)
                        lst.append(td.text)
            except Exception as msg:
                print(msg)

            driver.switch_to.window(driver.window_handles[0])   # 回到視窗1

    driver.quit()
    return lst   # 回傳課表
# 制別,科目,班級,開班／選課人數,任課教師,上課日期／節次,年級,教室【校區】,選別,學分,類別,畢業班,學期數
# print(driver.page_source)
# WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR , "body.table.tbody.tr:nth-child(4).td.a.img[name = 'menu_r1_c2']"))).click()

'''-----------------------------------------------------'''
def main():
    # 輸入
    # semester = input('請輸入學期編號(1:上學期 2:下學期)')
    semester = '1'
    
    # driver.quit()

    lst = []
    lst=Compulsory(semester)
    lst=Elective(semester,lst)
    lst=General_Education(semester,lst)
    col = 13
    lst = [lst[i:i + col] for i in range(0, len(lst), col)]
    df = pd.DataFrame(lst)
    print(df)
    now = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())) 
    df.to_csv('demo-'+now+'.csv', encoding='utf-8-sig', index=False, header=False)
    # time.sleep(5)

schedule.every().minute.at(':10').do(main)

while True:
    schedule.run_pending()
    time.sleep(5)