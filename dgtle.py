import os 
import requests 
from bs4 import BeautifulSoup 

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
URL = 'https://www.dgtle.com/article-1588130-1.html' #The target webpage


if 'inst' in URL:
    
    print('Inst type found')
    print('Downloading')
    # inst author
    html = requests.get(URL)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, 'lxml')
    name = soup.select('div.own-img > div:nth-child(2) > span:nth-child(1)')
    for n1 in name:
        dir_name = n1.get_text()

    # inst image
    ori_url_a1 = soup.find_all('div', class_='bg-img')
    downlist = []
    for a1 in ori_url_a1:
        ori_url_a2 = a1['data-src']
        real_url_a = ori_url_a2.replace('_1800_500','')
        downlist.append(real_url_a)

elif 'article' in URL:

    print('Article type found')
    print('Downloading')
    # article author
    html = requests.get(URL)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, 'lxml')
    name = soup.select('.author')
    for n2 in name:
        dir_name = n2.get_text()
        
    # article image
    ori_url_b1 = soup.select('.articles-comment-left > figure > img')
    downlist = []
    for b1 in ori_url_b1:
        ori_url_b2 = b1['src']
        real_url_b = ori_url_b2.replace('_1800_500','')
        downlist.append(real_url_b)

else:
    print('There is no key words in URL, please add new code to fix it.')

if not os.path.exists(dir_name):
    os.mkdir(dir_name)

for url in downlist:
    file_name=url.split("/")[-1]
    meizi=requests.get(url,headers=header)
    with open(dir_name+'/'+file_name,'wb') as f:
        f.write(meizi.content)
