# import webdriver 
import openpyxl.workbook
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
import openpyxl
import pandas as pd
import subprocess
from subprocess import CREATE_NO_WINDOW




def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    # return webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    return webdriver.Chrome(options=options)

def compare_data(archive_file, url):



    return

def get_sections():

    print('Gathering Sections..........')
    sections = {}

    driver = get_driver()
    driver.get('https://manilastandard.net/')

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


def scraper(sections):

    # sections = {'News':'https://manilastandard.net/category/news'}

    _file = Path(__file__).parent/f'Data/Manila Standard Online/Archive/Archive.xlsx'
    # archive_xlsx = openpyxl.load_workbook(_file)
    archive_data = pd.read_excel(_file)

    df = pd.DataFrame()
    df['Title'] = ''
    df['URL'] = ''
    
    driver = get_driver() 
    
    j = 0
    for k, v in sections.items():
        driver.get(v)

        # driver.execute_script("window.scrollTo(0, 1080)")
        html = driver.find_element(By.TAG_NAME, 'html')

        count = 0
        while count < 2:
            html.send_keys(Keys.END)
            time.sleep(5)
            count += 1
        

        elements = driver.find_elements(By.CLASS_NAME, 'entry-title.td-module-title')

        l = 0
        for element in elements:
            ele = element.find_element(By.TAG_NAME, 'a')
            cat = ele.text
            link = ele.get_attribute('href')
                

            if cat not in ['', None]:
                if any(archive_data.URL == link):
                    pass
                else:
                    df.at[j, 'Title'] = cat
                    df.at[j, 'URL'] = link
                    l += 1

            j += 1
        
        print(f'{k} - Found ({l} New Links)')
    
    driver.quit()
    
    # remove duplicate rowa    
    df.drop_duplicates(inplace=True)

    # conbine the new dataframe and archive
    new_df = pd.concat([df, archive_data], ignore_index=True)
    new_df.drop_duplicates(inplace=True)

    # save new dataframe to excel without indices
    new_df.to_excel(_file, index=False)

    # save extracted new extracted data to excel
    df.to_excel('Data/Manila Standard Online/New/Extracted_Links.xlsx', index=False)
    return


# main process
# scraper()
sections = get_sections()
scraper(sections)




# data = {
#   "name": ["Sally", "Mary", "John"],
#   "age": [50, 40, 30]
# }

# df = pd.DataFrame(data)
# print(df)

# if any(df.name == 'ally'):
# 	print('Found')
# else:
# 	data = [['ally','25']]
# 	df1 = pd.DataFrame(data, columns=['name','age'])

# new_df = df1.append(df)
# new_df.reset_index(drop=True, inplace=True)
# print(new_df)
