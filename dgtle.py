import os
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait
import logging


"""
Create an empty folder, that contains all the webpage url shortcuts from Dgtle.com
Copy and run this py file from that folder.

images will be downloaded as their original resolution and 
stored into each folder by author's id.
"""

# 12/31/2024
# 6:49 PM


# Configuration
LOGFILE_PATH = os.path.join(os.getcwd(), "dgtle.log")
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
MAX_RETRIES = 10
THREAD_POOL_SIZE = 8


# Logging setup
def setup_logging():
    # Create the logger
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(
        filename=LOGFILE_PATH, mode="a", encoding="utf-8")
    console_handler = logging.StreamHandler()

    # Define separate formats
    file_format = logging.Formatter(
        "%(asctime)s %(levelname)s %(lineno)d %(message)s")
    console_format = logging.Formatter("%(message)s")

    # Set formats to handlers
    file_handler.setFormatter(file_format)
    console_handler.setFormatter(console_format)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Add a utility function to the logger for inserting empty lines
    def insert_empty_line():
        file_handler.stream.write("\n")
        file_handler.flush()  # Ensure the newline is immediately written to the file

    # Attach the utility to the logger
    logger.insert_empty_line = insert_empty_line


# Get webpage URLs from shortcuts
def internet_shortcut(rootdir=os.getcwd()):
    '''
    GET WEBPAGE URL FROM SHORTCUT LINKAGES IN CERTAIN FOLDER.
    '''
    webpage_list = {}
    for _, _, filenames in os.walk(rootdir):
        for filename in filenames:
            if filename.lower().endswith('.url'):
                try:
                    with open(os.path.join(rootdir, filename), "r", encoding='utf-8') as f:
                        webpage = f.read().split('\n')[1][4:]
                        # Just be sure the data we acquired is URL
                        if webpage.startswith('http'):
                            webpage_list[webpage] = filename
                except Exception as e:
                    logger.warning(f"Error reading shortcut {filename}: {e}")
    return webpage_list


# Used for test and troubleshooting
def get_soup_from_localhtml(webpage):
    soup = BeautifulSoup(open(webpage, encoding='utf-8'), features='lxml')
    return soup


def find_author(soup):
    '''
    FIND AUTHOR AND USE IT AS FOLDER'S NAME.
    '''
    # This is for Inst page, and if it is not, which will return None
    if soup.find('div', class_='interset-content-top'):
        # In that case, skip this line, goto next condition
        author = soup.find(
            'div', class_='interset-content-top').get_text().strip().split("\n")[0]
    else:  # Choose Article page instead.
        author = soup.find('span', class_='author').get_text()
    return author


def extract_image_url(soup):
    '''
    EXTRACT IMAGE URL USING BS4.
    '''
    downlist = set()

    # Some articles have a comment area below them
    # which will include pictures from the author's other articles
    # and may even include pictures attached by commenters
    # The code here is used to remove the entire comment area
    # including "More articles by XXXX"
    comment_hot_new_warp = soup.find('div', class_="comment-hot-new-warp")
    if comment_hot_new_warp:
        comment_hot_new_warp.decompose()

    try:
        for img_tag in soup.find_all('img'):
            # If "src" doesn't exist, return an empty string "" (the default value)
            raw_img_url = img_tag.get(
                'data-original') or img_tag.get('src', '')

            if raw_img_url:
                img_url = raw_img_url.replace("_1800_500_w.", ".").replace(
                    "_1800_500.", ".").split("?")[0]

                # if 'dgtle_img/article' in img_url or 'dgtle_img/ins' in img_url or 'p3-sign.toutiaoimg.com' in img_url:
                if any(keyword in img_url for keyword in ["dgtle_img/article", "dgtle_img/ins", "p3-sign.toutiaoimg.com"]):
                    # uses downlist.add() (indicating downlist is a set)
                    downlist.add(img_url)

    except Exception as e:
        logger.warning(f"Error extracting images: {e}")

    if not downlist:
        logger.warning(
            "Nothing found, maybe they changed the code again. Let's upgrade the code too.")

    return list(downlist)


# Fetch and parse webpage
def get_soup_from_webpage(url, header, retries):
    '''
    USE BEAUTIFULSOUP TO PARSING HTML AND XML DOCUMENTS.
    DUE TO THE POOR SERVER CONNECTION, IT IS NECESSARY TO KEEP TRYING MULTIPLE TIMES.
    '''
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=header, timeout=15)
            response.encoding = "utf-8"
            return BeautifulSoup(response.text, "lxml")
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
            logger.info("Let's wait for 5 seconds.")
            time.sleep(5)
            logger.info("Let's back to work.")
    logger.critical(f"Failed to fetch {url} after {retries} attempts.")
    return None


def rillaget(link, dir_name, header, retries=8):
    filename = link.split("/")[-1]
    if ".image" in filename:  # toutiaoimg.com
        filename = filename.split(".")[0]

    for attempt in range(retries):
        try:
            response = requests.get(link, headers=header, timeout=10)

            if response.status_code == 200:
                # Get content type and set proper extension
                content_type = response.headers.get('Content-Type', '')
                extentions = ['.jpg', '.png', '.jpeg', '.gif', '.webp']
                if not any(ext in filename.lower() for ext in extentions):
                    image_format = content_type.split('/')[-1]
                    filename = f"{filename}.{image_format}"

                total_path = os.path.join(dir_name, filename)
                expected_length = int(
                    response.headers.get('Content-Length', 0))
                current_length = 0

                with open(total_path, 'wb') as f:
                    # Increased chunk size for better performance
                    for chunk in response.iter_content(8192):
                        f.write(chunk)
                        current_length += len(chunk)

                # Verify file size after download
                if expected_length > 0 and current_length >= expected_length:
                    logger.info(f"{filename}  Downloaded.")
                    return True

            elif response.status_code == 403:
                logger.warning(f"Access forbidden (403) for {filename}")
                time.sleep(5)
                continue

            # Other status codes
            logger.warning(
                f'Network error {response.status_code} occurred while trying to download {link}, waiting {5 * (attempt + 1)} seconds before making {attempt + 1}th attempt')
            time.sleep(5 * (attempt + 1))

        except requests.RequestException as e:
            logger.error(
                f'Network error {response.status_code} occurred while trying to download {link}, waiting {5 * (attempt + 1)} seconds before making {attempt + 1}th attempt')
            time.sleep(5 * (attempt + 1))

    # If all retries failed
    logger.error(f"{filename} Failed to download.")
    return False


def main():
    webpage_list = internet_shortcut()
    with ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
        for weblink, shortcut in webpage_list.items():

            logger.info(weblink)
            logger.info(shortcut)

            soup = get_soup_from_webpage(weblink, header, retries=MAX_RETRIES)
            title = soup.title.get_text()
            logger.info(f"\n{title}")

            if title == " 数字尾巴 分享美好数字生活":
                logger.critical("The post was probably harmonized.")
                continue

            if "无法找到内容" in soup.get_text() or "内容已删除或正在审核" in soup.get_text():
                logger.critical(
                    "The content cannot be found or has been deleted or is under review. Sorry, next one!")
                continue

            dir_name = find_author(soup)
            downlist = extract_image_url(soup)

            logger.info(f'Author is: {dir_name}')
            logger.info(f'Found {len(downlist)} Images')

            if not downlist:
                logger.critical("downlist is not existing.")
                continue

            os.makedirs(dir_name, exist_ok=True)

            # Submit all downloads for this webpage and wait for them to complete
            futures = [executor.submit(
                rillaget, link, dir_name, header) for link in downlist]
            # Wait for all downloads from this webpage to complete
            wait(futures)

            logger.insert_empty_line()


if __name__ == '__main__':
    logger = logging.getLogger()
    setup_logging()
    header = {"User-Agent": USER_AGENT}
    main()
