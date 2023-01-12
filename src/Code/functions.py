def import_libraries():    
    '''
    Imports libraries needed for webscraping, making soup, using BGG_Client, and creating graphics.
    Tested on Python 3.10.6
    User may also require the following modules:
    #!pip install selenium
    #!pip install webdriver-manager
    #!pip install lxml  
    #!pip install plotly --upgrade
    #!pip install dataframe_image
    #!pip install -U kaleido
    '''
    from bs4 import BeautifulSoup as bs
    import requests
    from datetime import datetime
    import re
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    from webdriver_manager.chrome import ChromeDriverManager

    import boardgamegeek
    from boardgamegeek import BGGClient

    import pandas as pd
    import numpy as np
    import seaborn as sns
    import altair as alt
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    import plotly.graph_objects as go
    import dataframe_image as dfi

    import warnings
    warnings.filterwarnings("ignore")

    print(datetime.now())

def url_creator(from_page, to_page):
    '''
    creates a list of URLS after first page to query with Selenium
    '''
    urls = []
    #end_range = int(upto_page)
    for i in range(from_page, (to_page + 1)):
        #print(from_page, to_page)
        #print(i)
        urls.append(f"https://boardgamegeek.com/browse/boardgame/page/{i}")
    return urls