import os 
import time
import urllib.request
import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.dgtle.com/inst-1689143-1.html"
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}

for i in range(1,2):
    try:
        request=urllib.request.Request(URL,headers=header)
        content = urllib.request.urlopen(request).read()
        data = content.decode('utf-8')
        soup = BeautifulSoup(data, 'lxml')

        # Print Title of the page
        title = soup.title.get_text()
        print(title)

        # Extract the hi resolution image url
        re_img_url = r"(?<=img src=\").+?dgtle_img.+?(?=\")"
        urls = re.findall(re_img_url, data)

        downlist = []
        for url in urls:
            url_hi = url.replace('_1800_500','')
            downlist.append(url_hi)

            if 'inst' in URL:
                # inst author
                name = soup.select('div.own-img > div:nth-child(2) > span:nth-child(1)')
                title = soup.title.get_text()
                for n1 in name:
                    dir_name = n1.get_text()

            elif 'article' in URL:
                # article author
                name = soup.select('.author')
                title = soup.title.get_text()
                for n2 in name:
                    dir_name = n2.get_text()
            else:
                # Just in case a new format is shown
                print('There is no key words in URL, please add new code to fix it.')
    except:
        print("Links extracting failed..")
        print("Wait for 5 seconds")
        time.sleep(5)
        print("Continue...")
        continue


    print(dir_name)

# Create the folder with the author's id
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

for url in downlist:
    file_name = url.split("/")[-1]
    with open(dir_name+'/'+ file_name, 'wb') as handle:
        response = ''
        while response == '':
            try:
                response = requests.get(url, stream=True, verify=False, headers=header)
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
