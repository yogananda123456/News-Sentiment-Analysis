
keyword = input("Enter any keyword: ")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

#chromedriver_path = 'C://chromedriver.exe'
#service = Service(chromedriver_path)
driver = webdriver.Chrome()

url = f'https://www.google.com/search?q={keyword}&tbm=nws'
driver.get(url)

news_results = driver.find_elements(By.CSS_SELECTOR, 'div#rso > div >div>div>div')
all_news_links = []
for news_div in news_results:
    news_item = []
    try:
        news_link = news_div.find_element(By.TAG_NAME, 'a').get_attribute('href')
       # print("Link:", news_link)
        #news_item[0] = news_link
        all_news_links.append(news_link)

        divs_inside_news = news_div.find_elements(By.CSS_SELECTOR, 'a>div>div>div')

        for new in divs_inside_news:
            news_item.append(new.text)
       # print("Domain:", news_item[1])
       # print("Title:", news_item[2])
       # print("Description:", news_item[3])
       # print("Date:", news_item[4])
       # print("-"*50+"\n\n"+"-"*50)
        #all_news.append(news_item)
    except Exception as e:
        print("No Elems")


driver.quit()

import pandas as pd
df = pd.DataFrame(all_news_links)

import requests
import csv
from bs4 import BeautifulSoup
import os
import spacy
#spacy.cli.download('en_core_web_sm')
nlp = spacy.load('en_core_web_sm')

url = df[0][0]

#getting requested data from the site 
response=requests.get(url)
#extracting text from response
response.encoding = 'utf-8'
html = response.text
#intialising soup
soup =  BeautifulSoup(html,features="html.parser")
text = soup.get_text()
#cleaning text 
clean_text= text.replace("/n", " ")       
clean_text= ''.join([c for c in clean_text if c != "'"])
#getting the text into sentences
sentences=[]
tokens = nlp(clean_text)
for sent in tokens.sents:
    sentences.append((sent.text.strip()))

#sentences  

filename = "Analyse.csv"

with open(filename, "w", newline="",encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["lines"])
    for sentence in sentences:
        writer.writerow([sentence])
print()
print()
print("A CSV file is created under the name Analyse.csv in  Downloads.")
print("The sentiment analysis can be found by running streamlit run ex.py command")






