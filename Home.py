import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# scrapers
from scraper_mst import mst


with st.sidebar:

    st.header('Links Scraper')

    pub_sel = st.radio(
        'Select Online Publication to scrape',
        ('Manila Bulletin',
        'Inquirer.net',
        'Philstar',
        'Business Mirror',
        'Business World',
        'Manila Times',
        'Manila Standard',
        'Malaya Business Insight',
        'Daily Tribune'))

    pro = st.button(label='Process')


if pro:
    if pub_sel == 'Manila Standard':
        mst()

    else:
        st.error('Development Phase')