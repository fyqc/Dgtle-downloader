import os 
import time
import requests
from bs4 import BeautifulSoup

'''
Put all webpage url shorcuts into the same folder this py file located.
Then use Powershell / Cmd to run py file.
images will be downloaded as their original resolution and 
stored into each folder by author's id.
'''

# 2/25/2021 
# 11：23 PM

# Set current py folder as working folder with os package.
rootdir=os.curdir 

def urltotxt():
    '''
    Convert url to text, and save it as a temporary file "load.txt"
    '''
    for (_,_,filenames) in os.walk(rootdir):
        for filename in filenames:
            with open(rootdir + '\\'+ filename, "r", encoding='utf-8') as infile:
                for line in infile:
                    if (line.startswith('URL')):
                        url = line[4:]
                        print(url, end='', file=open(rootdir + '/' + "load.txt", "a"))
                        break

def txttourl(path):
    '''
    Extracting txt of each article from that temporary file "load.txt"
    :path is current folder where your py file located.
    :return result
    '''
    result=[]
    with open(path,'r') as f:
        for line in f:
            result.append(list(line.strip('\n').split(',')))
    return result

def dgtsoup(URL, header):
    '''
    Use 'BeautifulSoup' & 'lxml' to parsing html
    :URL & header is the input
    :return soup.
    '''
    response = requests.get(URL, headers=header)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    return soup

def dgttitle(soup):
    '''
    Use Inst author as dir_name
    :soup is the input from dgtsoup(url)
    :return dir_name
    '''
    title = soup.title.get_text()
    return title

def dgtinst_author(soup):
    '''
    Use Inst author as dir_name
    :soup is the input from dgtsoup(url)
    :return dir_name
    '''
    author = soup.find_all('div', class_='userinfo-pop-up-name')
    author_bf = BeautifulSoup(str(author[0]), 'lxml')
    author_id = author_bf.find_all('span')
    for n in author_id:
        dir_name = n.get_text()
    return dir_name

def dgtinst_img(soup):
    '''
    Inst image link add to downlist
    :soup is the input from dgtsoup(url)
    :return downlist
    '''
    downlist = []
    tag_div = soup.find_all('div', class_='bg-img')
    div_bf = BeautifulSoup(str(tag_div), 'lxml')
    tag_img = div_bf.find_all('img')
    for x in tag_img:
        img_url = x.get('src')
        img_url = img_url.replace('_1800_500','')
        downlist.append(img_url)
    return downlist

def dgtartc_author(soup):
    '''
    Use article author as dir_name
    :soup is the input from dgtsoup(url)
    :return dir_name
    '''
    author = soup.find_all('span', class_='author')
    for n in author:
        dir_name = n.get_text() 
    return dir_name

def dgtartc_img(soup):
    '''
    Article image link add to downlist
    :soup is the input from dgtsoup(url)
    :return downlist
    '''
    downlist = []    
    tag_div = soup.find_all('div', class_='articles-comment-left forum-viewthread-article-box')
    div_bf = BeautifulSoup(str(tag_div[0]), 'lxml')
    tag_img = div_bf.find_all('img')
    for x in tag_img:
        img_url = x.get('data-original')
        img_url = img_url.replace('_1800_500','')
        downlist.append(img_url)
    return downlist

def dgturl(URL,soup):
    '''
    Execute the image analyze.
    :use URL to initial the start sequnce
    :return dir_name and downlist
    '''
    if 'inst' in URL:
        dir_name = dgtinst_author(soup)
        downlist = dgtinst_img(soup)
    elif 'article' in URL:
        dir_name = dgtartc_author(soup)
        downlist = dgtartc_img(soup)
    else:
        print('There is no key words in URL, please add new code to fix it.')
    return dir_name, downlist

def dgttrysoup(URL, header):
    '''
    Use BS to findout the author id and use it as dir_name
    :use URL & header as input
    :return dir_name and downlist
    '''
    attemp_bf = 0
    success_bf = False
    while attemp_bf < 10 and not success_bf:
        try:
            soup = dgtsoup(URL, header)
            title = dgttitle(soup)
            print(title)
            dgturl_result = dgturl(URL, soup)
            dir_name = dgturl_result[0]
            downlist = dgturl_result[1]
            print(f'Author is: {dir_name}')
            print(f'Found {len(downlist)} Images')
            success_bf = True
        except:
            attemp_bf += 1
            print("Links extracting failed..")
            print("Wait for 5 seconds")
            time.sleep(5)
            print("Continue...")
            if attemp_bf == 10:
                break
    return dir_name, downlist


def dgtdownload(dir_name, downlist, header):
    '''
    Distributing download files with their link
    :use dir_name, downlist, header as inputs
    '''

    t1 = time.time() # Start time count
    filenumber = 0
    total_number = len(downlist)
    filenumber = dgtdownloading(filenumber, downlist, dir_name)
    failnumber = total_number - filenumber
    t2 = time.time()-t1 # Finish time count
    print(f'{filenumber} files downloaded, took: {t2:.2f} seconds.')
    
    if failnumber > 0:
        print(f'Warning，There are {failnumber} files failed to be downloaded.')
    print()

def dgtdownloading(filenumber, downlist, dir_name):
    '''
    Monitoring download process
    :use filenumber, downlist and dir_name as inputs
    :return filenumber
    '''
    while len(downlist)>0:
        url = downlist.pop() 
        file_name = url.split("/")[-1]
        attempts = 0
        success = False
        while attempts < 5 and not success:
            try:
                t3 = time.time()
                success = dgtdownloader(url, file_name, dir_name, header) 
                filenumber += 1
                t4 = time.time()-t3
                print(f' {t4:.2f} Seconds used.') 
            except:
                print('Download failed, Retrying')
                attempts += 1
                if attempts == 5:
                    break
    return filenumber

def dgtdownloader(url, file_name, dir_name, header):
    '''
    Downloader, try my best to download a complete image due to the awful server connection.
    :use url, file_name, dir_name, header as inputs
    :return success status
    '''
    response = requests.get(url, headers=header, verify=False, timeout=30)
    if response.status_code == 200 and not os.path.exists(dir_name): 
        os.mkdir(dir_name)        
    total_path = dir_name + '/' + file_name
    
    if 'Content-Length' in response.headers and len(response.content) == int(response.headers['Content-Length']):
        with open(total_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
            f.close()
        print(file_name + " successfully downloaded.")

    else:
        print("The image has risk of incomplete")
        with open(total_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
            f.close()
        print(file_name + "successfully downloaded.")
    success = True
    return success

def dgtplay(URL, header):
    '''
    Start the whole sequence.
    :use URL, header as inputs
    :no return
    '''
    soup = dgttrysoup(URL, header)
    dir_name = soup[0]
    downlist = soup[1]
    dgtdownload(dir_name, downlist, header)


if __name__ == '__main__':    
    path = 'load.txt'
    urltotxt()
    result = txttourl(path)
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    for x in result:
        URL = x[0]
        print('The web that open: ' + URL)
        dgtplay(URL, header)
        
# Delete the temporary load.txt from current folder.
    if os.path.exists('load.txt'):
        os.remove('load.txt')
