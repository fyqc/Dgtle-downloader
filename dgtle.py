import os 
import time
import requests
from bs4 import BeautifulSoup
from threading import Thread

"""
In default, you shall put all the webpage url shortcuts at 
D:\\RMT\\DGT
And you can run this py file anywhere.

To change the target path, go to the bottom, and change it as per your need.
Then use Powershell / Cmd to run py file.
images will be downloaded as their original resolution and 
stored into each folder by author's id.
"""

# FYQ
# 4/27/2021
# 10:04 PM

# GET WEBPAGE URL FROM SHORTCUT LINKAGES IN CERTAIN FOLDER
def internet_shortcut(rootdir):
    webpage_list = []
    for (_,_,filenames) in os.walk(rootdir):
        for filename in filenames:
            if filename.endswith('.URL'):
                with open(rootdir + '/'+ filename, "r", encoding='utf-8') as f:
                    webpage = f.read().split('\n')[1][4:]
                    if webpage.startswith('http'):
                        webpage_list.append(webpage)
    return webpage_list

# USE BEAUTIFULSOUP TO PARSING HTML AND XML DOCUMENTS
def get_soup_from_webpage(url, header):
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8' 
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    return soup

def get_soup_from_localhtml(webpage):
    soup = BeautifulSoup(open(webpage, encoding='utf-8'), features='lxml')
    return soup

# FIND TITLE USING BS4
def find_title(soup):
    web_title = soup.title.get_text()
    return web_title

# FIND AUTHOR AND USE IT AS FOLDER'S NAME
def find_author(soup):
    # This is for Inst page, and if it is not, which will return None
    if soup.find('div', class_='interset-content-top'): 
        # In that case, skip this line, goto next condition
        author = soup.find('div', class_='interset-content-top').get_text().strip().split("\n")[0] 
    else: # Choose Article page instead.
        author = soup.find('span', class_='author').get_text()
    return author

# EXTRACT IMAGE URL USING BS4
def extract_image_url(soup):
    downlist = []
    # Some Article has comment section underneath, comes with the referred images from other pages.
    # and occasionally, visitor can comment with images.
    # Here the codes used to removed such images.
    # Try...Except... used here to prevent any potential warning and mistakes.
    try:
        soup.find('div', class_="comment-hot-new-warp").decompose()
    except:
        pass
    
    tags = soup.find_all('img')
    for n in tags:

        # Article Type
        if n.get('data-original'):
            raw_img_url = n.get('data-original')
        # Inst Type and majority of Article Type
        elif n['src']:
            raw_img_url = n.get('src')
        img_url = raw_img_url.replace('_1800_500','').split("?")[0]

        if 'dgtle_img/article' in img_url or 'dgtle_img/ins' in img_url:
            downlist.append(img_url)
    
    if len(downlist) == 0:
        print("Nothing found here, it's time to update code.")
    
    # Remove duplicated images, just incase.
    downlist = list(set(downlist))
    return downlist

# DUE TO THE POOR SERVER CONNECTION, IT IS NECESSARY TO KEEP TRYING MULTIPLE TIMES
def try_soup_ten_times(url, header):
    soup_attemp = 0
    success_status = False
    while soup_attemp < 10 and not success_status:
        try:
            soup = get_soup_from_webpage(url, header)
            title = find_title(soup)
            print(title)
            dir_name = find_author(soup)
            downlist = extract_image_url(soup)
            print(f'Author is: {dir_name}')
            print(f'Found {len(downlist)} Images')
            success_status = True
        except:
            soup_attemp += 1
            print("Seems the network is not very stable...")
            print("Let's wait for 5 seconds.")
            time.sleep(5)
            print("Ok, let's try again.")
            if soup_attemp == 10:
                print("Well, I guess we just let it go.")
                break
    return dir_name, downlist

def make_folder_asper_author(dir_name):
    if not os.path.exists(dir_name): 
        os.mkdir(dir_name)

# THE CORE OF THIS CODE IS DOWNLOAD IMAGE W/O ANY ISSUES.
def rillaget(url, dir_name):
    # This is actually the biggest improve. to let one function carried out only one task.
    # This also makes the multithreading possible.
    filename = url.split("/")[-1]
    total_path = dir_name + '/' + filename
    attempts = 0
    success = False
    while attempts < 5 and not success:
        try:
            response = requests.get(url)
            if len(response.content) == int(response.headers['Content-Length']):
                with open(total_path, 'wb') as fd:
                    for chunk in response.iter_content(1024):
                        fd.write(chunk)
                print(filename + "  Successfully downloaded")
                success = True
            else:
                print("image might not received complete, will try one more time.")
        except:
            attempts += 1
            if attempts == 5:
                print(filename + 'failed to download.')
                break

if __name__ == '__main__':
    rootdir=r'D:\RMT\DGT'  # <<<< CHANGE HERE TO THE FOLDER YOU PUT THE URL SHORTCUTS
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}

    webpage_list = internet_shortcut(rootdir)
    for URL in webpage_list:
        dir_name, downlist = try_soup_ten_times(URL, header)
        make_folder_asper_author(dir_name)
        threads = []
        for url in downlist:
            t = Thread(target = rillaget, args = [url, dir_name])
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
