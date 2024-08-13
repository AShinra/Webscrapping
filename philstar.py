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
import datetime


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

    sections = {'Headlines':'https://www.philstar.com/headlines',
                'Opinion':'https://www.philstar.com/opinion',
                'Business':'https://www.philstar.com/business',
                'Nation':'https://www.philstar.com/nation',
                'News Commentary':'https://www.philstar.com/news-commentary',
                'Sports':'https://www.philstar.com/sports',
                'Entertainment':'https://www.philstar.com/entertainment',
                'Campus':'https://www.philstar.com/campus'}
                

    # sections = {'News Commentary':'https://www.philstar.com/news-commentary'}

    _file = Path(__file__).parent/f'Data/Philstar/Archive/Archive.xlsx'
    archive_data = pd.read_excel(_file)

    df = pd.DataFrame()
    df['Time'] = ''
    df['Section'] = ''
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
        
        # for carousel header
        try:
            carousel = driver.find_element(By.CLASS_NAME, 'carousel__items')
            carousel_items = carousel.find_elements(By.CLASS_NAME, 'carousel__item__title')
        except:
            pass
        else:
            for carousel_item in carousel_items:
                art_title = carousel_item.find_element(By.TAG_NAME, 'a').text
                art_url = carousel_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if any(archive_data.URL == art_url):
                    continue
                else:
                    df.at[j, 'Time'] = datetime.datetime.now()
                    df.at[j, 'Section'] = k
                    df.at[j, 'Title'] = art_title
                    df.at[j, 'URL'] = art_url
                    j += 1
        
        # scraper for body
        try:
            element = driver.find_element(By.CLASS_NAME, 'jscroll-inner')
            elements = element.find_elements(By.CLASS_NAME, 'news_title')
        except:
            pass
        else:
            for ele in elements:
                art_title = ele.find_element(By.TAG_NAME, 'a').text

                if art_title in ['', None]:
                    art_title = 'Title Not Available'
                # elif cat.lower() == k.lower():
                #     continue
        
                art_url = ele.find_element(By.TAG_NAME, 'a').get_attribute('href')

                # if 'philstar.com/authors' in link:
                #     continue
                
                if any(archive_data.URL == art_url):
                    continue
                else:
                    df.at[j, 'Time'] = datetime.datetime.now()
                    df.at[j, 'Section'] = k
                    df.at[j, 'Title'] = art_title
                    df.at[j, 'URL'] = art_url
                    j += 1
        
        # for news commentary body
        try:
            micro_bottom = driver.find_element(By.ID, 'micro_bottom')
            micro_bottom_articles = micro_bottom.find_elements(By.CLASS_NAME, 'microsite_article_title')
        except:
            pass
        else:
            for micro_bottom_article in micro_bottom_articles:
                art_title = micro_bottom_article.find_element(By.TAG_NAME, 'a').text
                art_url = micro_bottom_article.find_element(By.TAG_NAME, 'a').get_attribute('href')

                df.at[j, 'Time'] = datetime.datetime.now()
                df.at[j, 'Section'] = k
                df.at[j, 'Title'] = art_title
                df.at[j, 'URL'] = art_url
                j += 1

        # for news commentary header
        try:
            micro_top = driver.find_element(By.ID, 'micro_top')
            micro_top_articles = micro_top.find_elements(By.CLASS_NAME, 'microsite_article_title')
        except:
            pass
        else:
            for micro_top_article in micro_top_articles:
                art_title = micro_top_article.find_element(By.TAG_NAME, 'a').text
                art_url = micro_top_article.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if any(archive_data.URL == art_url):
                    continue
                else:
                    df.at[j, 'Time'] = datetime.datetime.now()
                    df.at[j, 'Section'] = k
                    df.at[j, 'Title'] = art_title
                    df.at[j, 'URL'] = art_url
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