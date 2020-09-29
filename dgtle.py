import os 
import time
import requests
from bs4 import BeautifulSoup 


header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
URL = input('Please enter the webpage address from www.dgtle:')

print('The web that open: ' + URL)

if 'inst' in URL:
    
    print('This webpage is Inst type')
    # inst author
    html = requests.get(URL)
    html.encoding = 'UTF-8'
    soup = BeautifulSoup(html.text, 'lxml')
    name = soup.select('div.own-img > div:nth-child(2) > span:nth-child(1)')
    title = soup.title.get_text()
    for n1 in name:
        dir_name = n1.get_text()
        print('The Author is: ' + dir_name)
        print('The webpage title is: ' + title)

    # inst image
    ori_url_a1 = soup.find_all('div', class_='bg-img')
    downlist = []
    for a1 in ori_url_a1:
        ori_url_a2 = a1['data-src']
        real_url_a = ori_url_a2.replace('_1800_500','')
        downlist.append(real_url_a)

elif 'article' in URL:

    print('This webpage is Article type')
    # article author
    html = requests.get(URL)
    html.encoding = 'UTF-8'
    soup = BeautifulSoup(html.text, 'lxml')
    name = soup.select('.author')
    title = soup.title.get_text()
    for n2 in name:
        dir_name = n2.get_text()
        print('The Author is: ' + dir_name)
        print('The webpage title is: ' + title)
    
    # article image
    ori_url_b1 = soup.select('.articles-comment-left > figure > img')
    ori_url_c1 = soup.find_all('div', class_='articles-comment-left')
    downlist = []
    for b1 in ori_url_b1:
        ori_url_b2 = b1['src']
        real_url_b = ori_url_b2.replace('_1800_500','')
        downlist.append(real_url_b)
    for c1 in ori_url_c1:
        c2 = c1.find_all('img')
        for n in range(0, len(c2)):
            c3 = c2[n].get('src')
            real_url_c = c3.replace('_1800_500','')
            downlist.append(real_url_c)


elif 'thread' in URL:

    print('This webpage is Thread type')
    # thread author
    html = requests.get(URL)
    html.encoding = 'UTF-8'
    soup = BeautifulSoup(html.text, 'lxml')
    name = soup.select('.author')
    title = soup.title.get_text()
    for n2 in name:
        dir_name = n2.get_text()
        print('The Author is ' + dir_name)
        print('The webpage title is: ' + title)
    
    # thread image
    ori_url_c1 = soup.find_all('div', class_='articles-comment-left')
    downlist = []
    for c1 in ori_url_c1:
        c2 = c1.find_all('img')
        for n in range(0, len(c2)):
            real_url_c = c2[n].get('src')
            downlist.append(real_url_c)

else:
    # Just in case a new format is shown
    print('There is no key words in URL, please add new code to fix it.')

#Remove the empty line in downlist
while '' in downlist:
    downlist.remove('')

#Remove emoji from downlist
for n in downlist:
    if 'dgtle' not in n:
        downlist.remove(n)

# Create the folder with the author's id
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

# Download the file from the url list
for url in downlist:
    file_name=url.split("/")[-1]

    with open(dir_name+'/'+ file_name, 'wb') as handle:
            response = ''
            while response == '':
                try:
                    response = requests.get(url, verify=False, headers=header, stream=True)
                    if not response.ok:
                        print(response)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
                    break
                except:
                    print("Connection dropped..")
                    print("Wait for 5 seconds")
                    time.sleep(5)
                    print("Continue...")
                    continue

print('Done, Wait for 2 seconds to start the next one.')
time.sleep(2)
