#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import os
import urllib
import re

kv={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
r=requests.get("https://www.dgtle.com/article-1578708-1.html",headers=kv)
soup = BeautifulSoup(r.text, 'lxml')

r.raise_for_status()
r.encoding=r.apparent_encoding

dir_name=re.findall('<span class="author">(.*?)</span>',r.text)[-1]

small_pic = soup.find('div', class_='articles-comment-left').find_all('img')

downlist = []
for a in small_pic:
    title = a.get_text()
    href = a['src']
    img_url = href

    if 'article' in img_url:
        img_name = img_url[:-14]
        ori_img_url = img_name + '.jpeg'
        downlist.append(ori_img_url)

    else:
        ori_img_url = img_url
        downlist.append(ori_img_url)


if not os.path.exists(dir_name):
    os.mkdir(dir_name)

for url in downlist:
    file_name=url.split("/")[-1]
    images=requests.get(url,headers=kv)
    with open(dir_name+'/'+file_name,'wb') as f:
        f.write(images.content)
