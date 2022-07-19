import itertools
from django.shortcuts import render
from django.http import HttpResponse
import os
from os import path
import string
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter, OrderedDict, defaultdict
from wordcloud import WordCloud,STOPWORDS
from tika import tika, parser
tika.TikaJarPath = r'D:\Profiles\20220170\AppData\Local\Temp'
# import PyPDF2
# import textract
from konlpy.tag import Okt
from PIL import Image
import numpy as np
import json
from itertools import islice
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import re
from ckonlpy.tag import Twitter
from datetime import datetime

from soynlp.utils import DoublespaceLineCorpus
from soynlp.noun import LRNounExtractor_v2
from soynlp.word import WordExtractor
# nltk.download('gutenberg')
# nltk.download('maxent_treebank_pos_tagger')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
import pandas as pd
import math

# df = pd.read_csv('./static/text/stopwords_KO2.csv', encoding="UTF-8") # encoding='cp949'
# df = pd.read_csv('./static/text/stopwords_KO2.csv', encoding='ISO-8859-1')
# # df.loc[-1] = '가'
# df.index = df.index + 1
# df = df.sort_index()
# df = df.rename(columns={'가': 'words'})

# 추가하고 싶은 Stopwords 입력 - 워드 클라우드에 반영
NewStopwords = ''
NewStopwords = set(NewStopwords.split(' '))
# idx = len(df.index)
# for word in NewStopwords :
#     if not (df['words']==word).any() : 
#         df.loc[idx] = word
#         idx += 1

# Create your views here.

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('D:/Profiles/20220170/django/chromedriver.exe', options=options) 
driver = webdriver.Chrome('chromedriver.exe', options=options) 
driver.implicitly_wait(20)

t = time.time()
driver.set_page_load_timeout(10)

url_list = []

datetype_today = datetime.today()
today = datetype_today.strftime('%Y.%m.%d')

mk_url_list = []
hk_url_list = []
url_dict = dict()
ja_url_dict = dict()

press_name = ""

## 사용자 사전에 명사 등록
twitter = Twitter()
twitter.add_dictionary(['메타버스', 'DBMS'], 'Noun')

# 불용어 사전 - 파일 읽어서 등록
global stopwords
stopwords = set(STOPWORDS)
st_file_path = r'D:\Profiles\20220170\django_workspace\newstoday\newstoday\static\text\stopwords_KO.txt'
with open(st_file_path, "r", encoding="UTF-8") as f:
    lines = f.read().splitlines()

for stw in lines:
    stopwords.add(stw)



def main(request):
  return render(request, 'main.html')


def crawling_today_cs(request):
    global today, url_dict, press_name
    cs_url_dict = dict()
    press_name = "조선일보"
    breaker = False    
    url = "https://www.chosun.com/economy/tech_it/"
    # result = requests.get(curr_url, verify=False)
    # soup = BeautifulSoup(result.content.decode('utf-8', 'replace'), "html.parser")
    # cards = soup.find("div", id="main")
    # print(cards)

    # 조선일보 - 테크 - 하루에 최대 3페이지 정도 올라올 것으로 가정하고 범위 설정. (cf. view상 1페이지는 page=0)
    # selenium driver 설정
    driver.implicitly_wait(20)

    for page in range(1, 4):       # 조선일보 page 1부터 시작 
        curr_url = url + "?page=" + str(page)             
        print("----------- 조선일보 target url: ", curr_url)    
        driver.implicitly_wait(10)
        driver.get(curr_url)

        # cards = driver.find_elements(By.CLASS_NAME, 'story-card-container')
        cards = driver.find_elements(By.CLASS_NAME, 'story-card__headline-container')
        for card in cards:
            aTag = card.find_element(By.TAG_NAME, 'a')

            article_title = aTag.find_element(By.TAG_NAME, 'span').text
            article_href = aTag.get_attribute('href')
            date = article_href[(len(url)):(len(url))+10]
            article_date = date.replace('/', '.')
            # 오늘자 기사 필터링
            if article_date != today:
                breaker = True
                break
            # print(article_date)     # 기사 발행일
            # print(article_title)    # 기사 제목
            # print(article_href)     # 기사 링크
            # print()
            cs_url_dict[article_title] = article_href   # key=제목, value=링크인 dict로 저장
        
        if breaker == True:
            break

    # print(cs_url_dict)
    url_dict = cs_url_dict
    return wordcloud_url(request)