#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import os
import urllib
import re



# headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
kv={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
# all_url = 'https://www.dgtle.com/article-1578708-1.html' # starting url
r=requests.get("https://www.dgtle.com/article-1578708-1.html",headers=kv)
# all_url = 'https://www.dgtle.com/article-1348577-1.html' # starting url
# 
# start_html = requests.get(all_url)  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
# print(start_html.text) ##打印出start_html (请注意，concent是二进制的数据，一般用于下载图片、视频、音频、等多媒体内容是才使用concent, 对于打印网页内容请使用text)
soup = BeautifulSoup(r.text, 'lxml')

r.raise_for_status()
r.encoding=r.apparent_encoding

# page_title = soup.title.text
# print(page_title) 

userid = soup.find('div', class_='info').find_all('span', class_='author')
for a in userid:
    simpleid = (a.text)

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
        # f = open(r'D:\RMT\DGT\download.txt', 'a')
        # print(ori_img_url, file=f)
        # new_url.append(ori_img_url)
    else:
        ori_img_url = img_url
        downlist.append(ori_img_url)
        # f = open(r'D:\RMT\DGT\download.txt', 'a')
        # print(ori_img_url, file=f)

if not os.path.exists(dir_name):
    os.mkdir(dir_name)
    # for url in ori_img_url:
    #     file_name=url.split("/")[-1]
    #     meizi=requests.get(url,headers=kv)
        
    #     with open(simpleid+'/'+file_name,'wb') as f:
    #         f.write(meizi.content)

for url in downlist:
    file_name=url.split("/")[-1]
    meizi=requests.get(url,headers=kv)
    with open(dir_name+'/'+file_name,'wb') as f:
        f.write(meizi.content)
'''
kv={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
r=requests.get("https://www.vmgirls.com/13734.html",headers=kv)

r.raise_for_status()
r.encoding=r.apparent_encoding
haha=re.findall('<a href="(.*?)" alt=".*?" title=".*?">',r.text)
dir_name=re.findall('<h1 class="post-title h3">(.*?)</h1>',r.text)[-1]
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
for url in haha:
    file_name=url.split("/")[-1]
    meizi=requests.get(url,headers=kv)
    with open(dir_name+'/'+file_name,'wb') as f:
        f.write(meizi.content)
'''