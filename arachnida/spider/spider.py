import requests as requests
import bs4 as bs4
import os as os
import argparse as argparse
import urllib as urllib


parser = argparse.ArgumentParser(
    description="Telecharger les images d'un site web"
)

parser.add_argument(
    "-r",
    action="store_true",
    help="exec recursif"
)

parser.add_argument(
    "-l",
    type=int,
    default=5,
    help="Len max pour telechargement recursif"
)

parser.add_argument(
    "-p",
    type=str,
    default="./data",
    help="Chemin pour save les images scrape"
)

parser.add_argument(
    "url",
    type=str,
    # default="https://books.toscrape.com/",
    help="URL du site a scraper"
)

args = parser.parse_args()
recursif = args.r
len_rec = args.l
folder_img = args.p
url_web = args.url

try:
    response = requests.get(url_web)
    if response.status_code == 200:
        if not os.path.exists(folder_img):
            os.makedirs(folder_img)
    else:
        print("here3")
        raise Exception

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    if recursif is True:
        counter = 1
    else:
        img = soup.find_all("img")
        counter = 1
        for img_tag in img:
            url_img = urllib.parse.urljoin(url_web, img_tag["src"])
            if url_img.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                res_img = requests.get(url_img)

                if res_img.status_code == 200:
                    ext = os.path.splitext(urllib.parse.urlparse(url_img).path)[1]
                    filename = f"image{counter}{ext}"
                    filepath = os.path.join(folder_img, filename)
                    with open(f"{filepath}", "wb") as f:
                        f.write(res_img.content)
                    counter += 1
except Exception as err:
    print("Error ->", err)
