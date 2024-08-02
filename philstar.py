import openpyxl.workbook
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
import openpyxl
import pandas as pd
import subprocess
from get_driver import get_driver


def get_sections():

    print('Gathering Sections..........')
    sections = {}

    driver = get_driver()
    driver.get('https://www.philstar.com/other-sections')

    # element = driver.find_element(By.CLASS_NAME, 'vc_row.tdi_268.wpb_row.td-pb-row.tdc-element-style')
    element = driver.find_element(By.CLASS_NAME, 'vc_row.tdi_279.wpb_row.td-pb-row.tdc-element-style')
    ele = element.find_elements(By.TAG_NAME, 'a')

    for i in ele:
        link = i.get_attribute('href')
        cat = i.text

        if cat not in ['', None, 'Users Agreement', 'Policy']:
            sections[cat] = link
    
    driver.quit()
    print(f'{len(sections)} Sections Found..........')

    return sections