import streamlit as st
import requests
from bs4 import BeautifulSoup

url = 'https://manilastandard.net/'
response = requests.get(url)

if response.status_code == 200:
    html_content = response.content
    # st.write(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')

    sub_header = soup.find(id='menu-ms-menu-desktop-2')
    sub_header_names = sub_header.find_all('a')

    section_dict = {}
    for i in sub_header_names:
        _url = i.get('href')
        if _url in [None, '', '#']:
            continue
        else:
            section_dict[i.text] = _url

else:
    print(response)


for k, v in section_dict.items():
    st.success(f'Scraing {k} Section')
    response = requests.get(v)

    if response.status_code == 200:
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        # sub_header = soup.find(class_=['vc_column','tdi_97','wpb_column','vc_column_container','tdc-column','td-pb-span8'])
        sub_header = soup.select('.tdb_module_loop.td_module_wrap.td-animation-stack.td-cpt-post')
        
        for i in sub_header:
            title = i.select('.entry-title.td-module-title')
            for j in title:
                st.write(j.find('a').get('href'))


    else:
        st.write('Loading Error')





