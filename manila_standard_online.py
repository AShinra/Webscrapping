# import webdriver 
import openpyxl.workbook
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import time
import openpyxl
import pandas as pd
import subprocess
from subprocess import CREATE_NO_WINDOW




def get_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--log-level=3")
    # return webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    return webdriver.Chrome(options=options)

def get_sections():

    sections = {}

    driver = get_driver()
    driver.get('https://www.manilastandard.net/')

    element = driver.find_element(By.CLASS_NAME, 'vc_row.tdi_268.wpb_row.td-pb-row.tdc-element-style')
    ele = element.find_elements(By.TAG_NAME, 'a')

    for i in ele:
        link = i.get_attribute('href')
        cat = i.text

        if cat not in ['', None, 'Users Agreement', 'Policy']:
            sections[cat] = link
    
    driver.quit()

    return sections


def scraper(sections):

    df = pd.DataFrame()
    df['Section'] = ''
    df['Title'] = ''
    df['URL'] = ''
    
    driver = get_driver() 
    
    j = 0
    for k, v in sections.items():
        driver.get(v)

        # driver.execute_script("window.scrollTo(0, 1080)")
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)

        time.sleep(5)

        elements = driver.find_elements(By.CLASS_NAME, 'entry-title.td-module-title')

        for element in elements:
            ele = element.find_element(By.TAG_NAME, 'a')
            link = ele.get_attribute('href')
            cat = ele.text

            if cat not in ['', None]:
                df.at[j, 'Section'] = k
                df.at[j, 'Title'] = cat
                df.at[j, 'URL'] = link

            j += 1
        
        print(f'{k} - Done')
    
    df.to_excel('Sample.xlsx', index=False)
 
    return


# main process
# scraper()
sections = get_sections()
scraper(sections)