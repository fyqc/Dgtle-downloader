import os
import time
import requests
from bs4 import BeautifulSoup
from threading import Thread

"""
Create an empty folder, that contains all the webpage url shortcuts from Dgtle.com
Copy and run this py file from that folder.

images will be downloaded as their original resolution and 
stored into each folder by author's id.
"""

# 4/4/2024
# 12:49 PM


def internet_shortcut(rootdir=os.getcwd()):
    '''
    GET WEBPAGE URL FROM SHORTCUT LINKAGES IN CERTAIN FOLDER.
    '''
    webpage_list = []
    for (_, _, filenames) in os.walk(rootdir):
        for filename in filenames:
            if filename.endswith('.URL'):
                with open(os.path.join(rootdir, filename), "r", encoding='utf-8') as f:
                    webpage = f.read().split('\n')[1][4:]
                    # Just be sure the data we acquired is URL.
                    if webpage.startswith('http'):
                        webpage_list.append(webpage)
    return webpage_list


def get_soup_from_webpage(url, header):
    '''
    USE BEAUTIFULSOUP TO PARSING HTML AND XML DOCUMENTS.
    '''
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


def find_title(soup):
    '''
    FIND TITLE USING BS4.
    '''
    return soup.title.get_text()


def find_author(soup):
    '''
    FIND AUTHOR AND USE IT AS FOLDER'S NAME.
    '''
    # This is for Inst page, and if it is not, which will return None.
    if soup.find('div', class_='interset-content-top'):
        # In that case, skip this line, goto next condition.
        return soup.find('div', class_='interset-content-top').get_text().strip().split("\n")[0]
    else:  # Choose Article page instead.
        return soup.find('span', class_='author').get_text()


def extract_image_url(soup):
    '''
    EXTRACT IMAGE URL USING BS4.
    '''
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
        # Article Type.
        if n.get('data-original'):
            raw_img_url = n.get('data-original')
        # Inst Type and majority of Article Type.
        elif n['src']:
            raw_img_url = n.get('src')
        # Here we trim the URL, for origin resolution.
        # On Jul 15, 2021, There is a new case found, the URL has no format attached,
        # as shown below, the real file which is jpg in fact.
        # http://s1.dgtle.com/dgtle_img/article/2021/07/15/74e7f202107151213512077_1800_500_w
        img_url = raw_img_url.replace('_1800_500_w.', '.').split("?")[0]
        img_url = img_url.replace('_1800_500.', '.').split("?")[0]

        if 'dgtle_img/article' in img_url or 'dgtle_img/ins' in img_url:
            downlist.append(img_url)

    if len(downlist) == 0:
        print("Nothing found here, website might been updated, it's time for us to update code.")

    # Remove duplicated images, just incase.
    downlist = list(set(downlist))
    return downlist


def try_soup_ten_times(url, header):
    '''
    DUE TO THE POOR SERVER CONNECTION, IT IS NECESSARY TO KEEP TRYING MULTIPLE TIMES.
    '''
    soup_attemp = 0
    success_status = False
    while soup_attemp < 10 and not success_status:
        try:
            soup = get_soup_from_webpage(url, header)
            title = find_title(soup)
            print(title)
            if title == " 数字尾巴 分享美好数字生活":
                print("This post might be deleted.")
            if "无法找到内容" in soup.get_text() or "内容已删除或正在审核" in soup.get_text():
                print("Well, let it go.")
                return ("404","404")
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
                print("Well, let it go.")
                return ("404","404")
    return dir_name, downlist


def make_folder_asper_author(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def rillaget(link, dir_name, header):
    '''
    THE CORE OF THIS CODE IS DOWNLOAD IMAGE W/O ANY ISSUES.
    '''
    filename = link.split("/")[-1]
    
    # On January 20, 2024, it was discovered that some pictures did not have suffixes, but were actually in jpeg format.
    # http://s1.dgtle.com/dgtle_img/article/2024/01/01/2e6b7202401012057028574_1800_500_w.Zuiko PRO」开向山的大门
    # On April 04, 2024, it was discovered that some pictures did not have suffixes, but were actually in jpeg format.
    # d7e06202403251246431344_1800_500_w.313
    
    extentions = ['.jpg', '.png', '.jpeg', '.gif']
    if not any(ext in filename for ext in extentions):
        filename = "".join([filename, '.jpeg'])
        
    total_path = os.path.join(dir_name, filename)
    attempts = 0
    success = False
    while attempts < 5 and not success:
        try:
            response = requests.get(link, headers=header, timeout=5)
            
            if len(response.content) == int(response.headers['Content-Length']):
                with open(total_path, 'wb') as fd:
                    for chunk in response.iter_content(1024):
                        fd.write(chunk)
                print(filename + "  Successfully downloaded")
                success = True
        except:
            print(f'{filename} has connection error, retry after 5 seconds for the {attempts + 1} attempts')
            time.sleep(5)
            attempts += 1
    if attempts == 5:
        print(f"{filename} Failed to downloaded.")


if __name__ == '__main__':
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}

    webpage_list = internet_shortcut()
    for weblink in webpage_list:
        dir_name, downlist = try_soup_ten_times(weblink, header)
        if downlist == "404":
            continue
        make_folder_asper_author(dir_name)
        threads = []
        for link in downlist:
            t = Thread(target=rillaget, args=[link, dir_name, header])
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
