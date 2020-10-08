import selenium
import pandas as pd
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime


def string_to_time_format(time_string: str):
    if 'Oct' in time_string:
        return time_string.replace('Oct', '10')
    elif 'Sep' in time_string:
        return time_string.replace('Sep', '09')
    elif 'Aug' in time_string:
        return time_string.replace('Aug', '08')
    else:
        return time_string


def get_competitor_data(competitor_id: str, max_days=30):
    today = datetime.datetime.now()
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.ebay.com/sch/' + competitor_id +
               '/m.html?_nkw&_armrs=1&_ipg&_from&LH_Complete=1&LH_Sold=1&rt=nc&_trksid=p2046732.m1684')
    driver.maximize_window()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                "//*[@id=\"gh-shipto-click\"]/div/button"))).click()
    time.sleep(0.5)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@class=\"menu-button\"]/button"))).click()
    dropDownOptions = driver.find_elements_by_xpath("//*[@class='menu-button__item']")
    dropDownOptionsNames = driver.find_elements_by_xpath("//*[@class='menu-button__item']/*/*[2]")
    time.sleep(0.5)
    dropDownOptions = {dropDownOptionsNames[i].text: dropDownOptions[i] for i in range(len(dropDownOptions))}
    dropDownOptions['United States'].click()
    time.sleep(0.5)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                "//button[@class='shipto__close-btn']"))).click()

    time.sleep(0.5)
    driver.refresh()
    time.sleep(1)

    sold_urls = driver.find_elements_by_xpath("//li[@class='sresult lvresult clearfix li']/h3/a")
    sold_times = driver.find_elements_by_xpath(
        "//li[@class='sresult lvresult clearfix li']/"
        "ul[@class='lvdetails left space-zero full-width']/li[@class='timeleft']/span")
    sold_names = [url.get_attribute('title') for url in sold_urls]
    sold_urls = [url.get_attribute('href') for url in sold_urls]
    sold_times = [datetime.datetime.strptime(string_to_time_format(t.text), '%m-%d %H:%M') for t in sold_times]
    table = pd.DataFrame(data={'url': sold_urls, 'title': sold_names})
    table['sold'] = 0
    table = table.groupby(by='title').agg({'sold': 'count', 'url': 'first'})
    table.to_csv('text.csv')
    driver.close()


get_competitor_data('trueproduct')

