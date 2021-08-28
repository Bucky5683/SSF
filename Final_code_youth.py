import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


import pandas as pd
import time
import threading


def selenium_run():
    result = final_code_youth()
    threading.Timer(5, selenium_run()).start()


def final_code_youth():
    start = time.time()

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    URL = 'https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do'
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    driver.get(URL)

    serchbox = driver.find_element_by_id('srchWord')
    serchbox.send_keys('지원금')
    serchbox.send_keys(Keys.RETURN)

    DF_youth = pd.DataFrame(columns=['title', 'href', 'age', 'area', 'work', 'rank', 'type'])

    paging = driver.find_element_by_class_name('paging')
    page_num = len(paging.find_elements_by_tag_name('a'))

    for page in range(1, page_num + 1):
        page_xpath = '//*[@id="srchFrm"]/div[5]/a[' + str(page) + ']'
        page_but = driver.find_element_by_xpath(page_xpath)
        page_but.click()

        num = driver.find_element_by_class_name('result-list-box').find_elements_by_tag_name('li')

        for index in range(1, len(num) + 1):

            xpath = '//*[@id="srchFrm"]/div[4]/div[2]/ul/li[' + str(index) + ']/a'
            e = driver.find_element_by_xpath(xpath)
            e.send_keys(Keys.ENTER)

            title = driver.find_element_by_class_name('plcy-left')
            title = title.text

            href = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[3]/ul/li[3]/div[2]/a')
            if href.text == "" or href.text == "-":
                href = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[4]/ul/li[4]/div[2]/a')
            href = href.text

            ul = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[2]/ul')
            list_cont = ul.find_elements_by_class_name('list_cont')
            나이 = list_cont[0].text
            거주지및소득 = list_cont[1].text
            학력 = list_cont[2].text
            전공 = list_cont[3].text
            취업상태 = list_cont[4].text

            DF_youth.loc[len(DF_youth.index)] = {'title': title, 'href': href, 'age': 나이, 'area': 거주지및소득, 'work': 학력,
                                                 'rank': 거주지및소득, 'type': "지원금"}
            driver.back()
            driver.refresh()

    end = time.time()
    print("소요시간 : ", (end - start) / 60)

    import sqlite3

    conn = sqlite3.connect('database.db', isolation_level=None)
    # c = conn.cursor()

    '''c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, \
              title text, href text, age text, area text, work text, \
              rank text, type text)")
    '''
    DF_youth.to_sql('youth', conn, if_exists='replace')
    driver.quit()

    return "finish"


selenium_run()
