import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd

name_list = []
fund_list = []
rating_list = []
review_list = []

url = base
iterator = 1
page = 1

response = requests.get(url)

if '200' in str(response):
    print("Success.")
    
soup = BeautifulSoup(response.text,"html.parser")
tags = soup.findAll("div",{"role":"listitem","class":"w-dyn-item"})

for i,tag in enumerate(tags):
    if i > 2:
        name_list.append(tag.h1.text.strip())
        fund_list.append(tag.h4.text.strip())
        rating_list.append(tag.h3.text.strip())
        review_list.append(tag.blockquote.text.strip())
    
while iterator != 0:
    url = base + "?3d70cb88_page=" + str(page)
    response = requests.get(url)
    
    if '200' not in str(response):
        print("Error!")
        print(response)
        iterator = 0
        break
    
    soup = BeautifulSoup(response.text,"html.parser")
    tags = soup.find_all("div",{"role":"listitem","class":"w-dyn-item"})
    
    if len(tags) == 3:
        print("End of data.")
        iterator = 0
        break
    
    for i,tag in enumerate(tags):
        if i > 2:
            name_list.append(tag.h1.text.strip())
            fund_list.append(tag.h4.text.strip())
            rating_list.append(tag.h3.text.strip())
            review_list.append(tag.blockquote.text.strip())
    
    time.sleep(30)
    page += 1

if len(name_list) == len(fund_list) == len(rating_list) == len(review_list):
    print("All lists equal.")
else:
    print("ERROR: Lists unequal.")

all_data = pd.DataFrame({'Name':name_list,\
                         'Fund':fund_list,\
                         'Rating':rating_list,\
                         'Review':review_list})

all_data.to_csv("all_vc_data.csv")

