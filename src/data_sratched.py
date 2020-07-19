import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import chardet
import os
from tqdm import tqdm

os.chdir('C:\\Users\\Simmons\\PycharmProjects\\cpc')

url = 'http://cpc.people.com.cn/GB/64162/64168/351850/index.html'

req = requests.get(url)

data = req.content
ns = BeautifulSoup(data, 'html.parser')
ns.prettify()
title = ns.find_all("a", attrs={"class": "red", 'target': '_blank'})

add_dict = {}
for i in range(len(title)):
    address = title[i].attrs['href']
    name = title[i].contents[0]
    add_dict[name] = address

content_df = pd.DataFrame(columns=['name', 'link', 'refer', 'order'])
for key, value in add_dict.items():
    url = value
    req = requests.get(url)
    data = req.content
    ns = BeautifulSoup(data, 'html.parser')

    title_i = ns.find_all("a", attrs={"class": "black", 'target': '_blank'})
    for t in range(len(title_i)):
        link = title_i[t].attrs['href']
        name = title_i[t].text  # 源代码写的不规范
        ser = pd.Series({'name': name, 'link': link, 'refer': value, 'order': key})
        content_df = content_df.append(ser, ignore_index=True)
    time.sleep(0.5)

for i in tqdm(content_df.index):
    href = content_df.loc[400, 'link']
    if href.count('http') > 0:
        url = href
    else:
        url = 'http://cpc.people.com.cn' + href
    req = requests.get(url)
    req.encoding = req.apparent_encoding
    data = req.content
    ns = BeautifulSoup(data, 'html.parser')
    text1 = ns.find_all("p")
    text2 = ns.find_all("p", attrs={"style": "text-indent: 2em;"})  # 网站源代码写的相当不规范，注意空格
    text1.extend(text2)
    texts = ''
    for j in range(len(text1)):
        try:
            te = text1[ j ].contents[ 0 ]
            texts += te
        except :
            pass
    content_df.loc[i, 'text'] = texts
    next_page = ns.find('div', attrs={'class': 'zdfy clearfix'})
    if next_page == None:
        content_df.loc[ i, 'next_page' ] = 0
    else:
        content_df.loc[ i, 'next_page' ] = 1
    time.sleep(0.5)



for i in tqdm(content_df.index):
    try:
        if content_df.loc[i, 'text'] == '':
            href = content_df.loc[i, 'link']
            if href.count('http') > 0:
                url = href
            else:
                url = 'http://cpc.people.com.cn' + href
            req = requests.get(url)
            req.encoding = req.apparent_encoding
            data = req.content
            ns = BeautifulSoup(data, 'html.parser')
            text1 = ns.find_all("p")
            texts = text1[1].text
            content_df.loc[i, 'text'] = texts
            time.sleep(0.5)
        else:
            pass
    except :
        pass

import re


def cut_out(a,b,string):
    result = re.findall(".*%s(.*)%s.*"%(a,b),string)
    return result


for i in content_df.index:
    name = content_df.loc[i, 'name']
    try:
        a = name.split('[')[1]
        b = a.split(']')[0]
        content_df.loc[ i, 'tag' ] = b
    except :
        pass


content_df.to_excel('./data_out/中共全国代表大会文本数据库.xlsx', encoding='gbk')
