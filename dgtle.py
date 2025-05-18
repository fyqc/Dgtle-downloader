from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tqdm import tqdm
from typing import Tuple
import logging
import time
import requests


"""
Create an empty folder, that contains all the webpage url shortcuts from Dgtle.com
Copy and run this py file from that folder.

images will be downloaded as their original resolution and 
stored into each folder by author's id.
"""

# 5/18/2025
# 03:01 AM

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0"
}


def setup_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[
            logging.FileHandler(
                filename="dgtle.log", mode="a", encoding="utf-8"
            )
        ],
    )


def internet_shortcut() -> list:
    """
    Get the "webpage URL" from the shortcut link in the current folder
    Return a dictionary of "URL" and "file name"
    """
    rootdir = Path.cwd()  # Get the current working directory as a Path object
    webpage_list = {}

    # Recursively find all .url files
    for filename in rootdir.glob("**/*.url"):
        try:
            with Path(filename).open(mode="r", encoding="utf-8") as f:
                webpage = f.read().split("\n")[1][4:]
                if webpage.startswith("http"):
                    webpage_list[webpage] = filename
        except Exception as e:
            logging.warning(f"Error reading shortcut {filename}: {e}")
            print(f"Error reading shortcut {filename}: {e}")

    return webpage_list


def get_soup_from_webpage(
    url: str, header: dict, retries: int = 5
) -> BeautifulSoup:
    """
    Use BEAUTIFULSOUP to parse HTML documents
    Generate "soup"
    Due to poor server connection, multiple attempts are required
    """
    for attempt in range(retries):
        try:
            if attempt == 0:
                logging.info(url)
                print(url)

            response = requests.get(url, headers=header, timeout=35)
            response.encoding = "utf-8"

            return BeautifulSoup(response.text, "lxml")

        except requests.RequestException as e:
            logging.warning(f" {url} failed {attempt + 1}th time: \n{e}")
            print(f" {url} failed {attempt + 1}th time")

            logging.info("Wait 5 seconds")
            print("Wait 5 seconds")

            time.sleep(5)

    logging.error(f"Could not fetch {url} after {retries} attempts")
    print(f"Could not fetch {url} after {retries} attempts")

    return None


def find_author(soup: BeautifulSoup) -> str:
    """
    FIND AUTHOR AND USE IT AS FOLDER'S NAME.
    """
    # This is for Inst page, and if it is not, which will return None
    if soup.find("div", class_="interset-content-top"):
        # In that case, skip this line, goto next condition
        author = (
            soup.find("div", class_="interset-content-top")
            .get_text()
            .strip()
            .split("\n")[0]
        )
    else:  # Choose Article page instead.
        author = soup.find("span", class_="author").get_text()
    return author


def extract_image_url(soup: BeautifulSoup) -> list:
    """
    EXTRACT IMAGE URL USING BS4.
    """
    downlist = set()

    # Some articles have a comment area below them
    # which will include pictures from the author's other articles
    # and may even include pictures attached by commenters
    # The code here is used to remove the entire comment area
    # including "More articles by XXXX"
    comment_hot_new_warp = soup.find("div", class_="comment-hot-new-warp")
    if comment_hot_new_warp:
        comment_hot_new_warp.decompose()

    try:
        for img_tag in soup.find_all("img"):
            # If "src" doesn't exist, return an empty string "" (the default value)
            raw_img_url = img_tag.get("data-original") or img_tag.get("src", "")

            if raw_img_url:
                img_url = (
                    raw_img_url.replace("_1800_500_w.", ".")
                    .replace("_1800_500.", ".")
                    .split("?")[0]
                )

                # if 'dgtle_img/article' in img_url or 'dgtle_img/ins' in img_url or 'p3-sign.toutiaoimg.com' in img_url:
                if any(
                    keyword in img_url
                    for keyword in [
                        "dgtle_img/article",
                        "dgtle_img/ins",
                        "p3-sign.toutiaoimg.com",
                    ]
                ):
                    # uses downlist.add() (indicating downlist is a set)
                    downlist.add(img_url)

    except Exception as e:
        logging.warning(f"Error extracting images: {e}")
        print(f"Error extracting images: {e}")

    return list(downlist)


def rillaget(link: str, dir_name: str, header: dict) -> Tuple[bool, str]:
    """
    A naive but slightly better self-made downloader
    """
    attempts = 0
    success = False
    while attempts < 8 and not success:
        try:
            response = requests.get(link, headers=header, timeout=(10, 60))
            response.raise_for_status()

            filename = link.split("/")[-1]

            if ".image" in filename:  # toutiaoimg.com
                filename = filename.split(".")[0]

            extensions = [".jpg", ".png", ".jpeg", ".gif", ".webp"]
            if not any(filename.endswith(ext) for ext in extensions):
                content_type = response.headers.get("Content-Type", "")
                if "/" in content_type:
                    image_format = content_type.split("/")[-1]
                    filename = f"{filename}.{image_format}"

            total_path = Path(dir_name) / filename

            with open(total_path, "wb") as f:
                f.write(response.content)
            return True, total_path

        except requests.exceptions.HTTPError as e:
            if attempts == 8:
                return False, str(e)
            wait_time = 5 * attempts + 5
            logging.error(
                f"Network error occurred while trying to download {link}, waiting {wait_time} seconds before making {attempts + 1}th attempt"
            )
            time.sleep(wait_time)
            attempts += 3

        except Exception as e:
            if attempts == 8:
                return False, str(e)
            wait_time = 5 * attempts + 5
            logging.error(
                f"Network error occurred while trying to download {link}, waiting {wait_time} seconds before making {attempts + 1}th attempt"
            )
            time.sleep(wait_time)
            attempts += 1


def download_all(downlist, dir_name, header, max_workers=16):
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(rillaget, link, dir_name, header)
            for link in downlist
        ]

        for link, future in tqdm(
            zip(downlist, futures), total=len(downlist), desc="Downloading"
        ):
            try:
                success, result = future.result()

                logging.info(
                    f"{link} {'Download successful' if success else 'Download failed'} -> {result}"
                )

            except Exception as e:
                logging.error(f"Error {link}: {e}")
                print(f"Error {link}: {e}")


if __name__ == "__main__":
    setup_logging()

    webpage_list = internet_shortcut()
    for webpage, shortcut in webpage_list.items():
        logging.info(shortcut)

        soup = get_soup_from_webpage(webpage, HEADER)

        if not soup:
            logging.critical("Failed to get soup, please check the code")
            print("Failed to get soup, please check the code")
            continue

        title = soup.title.get_text()
        logging.info(f"\n{title.lstrip()}")
        print(f"\n{title.lstrip()}")

        if title == " 数字尾巴 分享美好数字生活":
            logging.critical(
                "The post was probably deleted due to content review."
            )
            print("The post was probably deleted due to content review.")
            continue

        if (
            "无法找到内容" in soup.get_text()
            or "内容已删除或正在审核" in soup.get_text()
        ):
            logging.critical(
                "The content cannot be found or has been deleted or is under review. Sorry, next one!"
            )
            print(
                "The content cannot be found or has been deleted or is under review. Sorry, next one!"
            )
            continue

        dir_name = find_author(soup)
        downlist = extract_image_url(soup)

        logging.info(f"Author is: {dir_name}")
        print(f"Author is: {dir_name}")

        logging.info(f"Found {len(downlist)} images")
        print(f"Found {len(downlist)} images")

        if not downlist:
            logging.critical(
                "Nothing found, maybe they changed the code again."
            )
            print("Nothing found, maybe they changed the code again.")

        download_all(downlist, dir_name, HEADER)

        # Add blank lines to separate log and print output
        logging.info("\n" * 3)
        print("\n" * 2)
