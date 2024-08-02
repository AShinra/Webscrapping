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


def sections_ps():

    print('Gathering Sections..........')
    sections = {}

    driver = get_driver()
    driver.get('https://www.philstar.com/other-sections')

    # element = driver.find_element(By.CLASS_NAME, 'vc_row.tdi_268.wpb_row.td-pb-row.tdc-element-style')
    element = driver.find_element(By.CLASS_NAME, 'theContent')
    ele = element.find_elements(By.TAG_NAME, 'a')

    for i in ele:
        link = i.get_attribute('href')
        cat = i.text

        if cat not in ['', None, 'Users Agreement', 'Policy']:
            sections[cat] = link
    
    driver.quit()
    print(f'{len(sections)} Sections Found..........')

    return sections

def scraper_ps(sections):

    sections = {'headlines':'https://www.philstar.com/headlines'}

    _file = Path(__file__).parent/f'Data/Philstar/Archive/Archive.xlsx'
    archive_data = pd.read_excel(_file)

    df = pd.DataFrame()
    df['Title'] = ''
    df['URL'] = ''
    
    driver = get_driver()

    j = 0
    for k, v in sections.items():
        driver.get(v)

        html = driver.find_element(By.TAG_NAME, 'html')

        count = 0
        while count < 4:
            html.send_keys(Keys.END)
            time.sleep(3)
            count += 1
        
        carousel = driver.find_element(By.CLASS_NAME, 'carousel__items')
        carousel_items = carousel.find_elements(By.CLASS_NAME, 'carousel__item__title')
        for carousel_item in carousel_items:
            art_title = carousel_item.find_element(By.TAG_NAME, 'a').text
            art_url = carousel_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if any(archive_data.URL == art_url):
                continue
            else:
                df.at[j, 'Title'] = art_title
                df.at[j, 'URL'] = art_url
                j += 1

        element = driver.find_element(By.CLASS_NAME, 'jscroll-inner')
        elements = element.find_elements(By.CLASS_NAME, 'news_title')
        
        for ele in elements:
            cat = ele.find_element(By.TAG_NAME, 'a').text

            if cat in ['', None]:
                continue
            # elif cat.lower() == k.lower():
            #     continue
    
            link = ele.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # if 'philstar.com/authors' in link:
            #     continue
            
            if any(archive_data.URL == link):
                continue
            else:
                df.at[j, 'Title'] = cat
                df.at[j, 'URL'] = link
                j += 1
    
        print(f'{k} - {j} New links found')
    
    driver.quit()
    
    # remove duplicate rowa    
    df.drop_duplicates(inplace=True)

    # conbine the new dataframe and archive
    new_df = pd.concat([df, archive_data], ignore_index=True)
    new_df.drop_duplicates(inplace=True)

    # save new dataframe to excel without indices
    new_df.to_excel(_file, index=False)

    # save extracted new extracted data to excel
    df.to_excel('Data/Philstar/New/Extracted_Links.xlsx', index=False)



    return