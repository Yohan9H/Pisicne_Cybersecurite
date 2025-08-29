from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import requests as requests
import os as os
import argparse as argparse

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")


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
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    print("Driver initialise")
    
    url_to_scrape = url_web
    driver.get(url_to_scrape)

    print(f"Site : {driver.title}")

    if recursif is True:
        print("Mode récursif active") # Il faut faire maintenant la recusif et verifier les options si tout est correct
        pass
    else:
        print("Recherche des images...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"{len(images)} images trouvees ! Telechargement en cours")

        os.makedirs(folder_img, exist_ok=True)
        counter = 1
        for img_tag in images:
            img_src = img_tag.get_attribute('src')
            if not img_src:
                continue
            url_img = urllib.parse.urljoin(url_web, img_src)

            if url_img.lower().startswith('http'):
                try:
                    path = urllib.parse.urlparse(url_img).path
                    if path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                        res_img = requests.get(url_img, timeout=10)
                        if res_img.status_code == 200:
                            ext = os.path.splitext(path)[1]
                            if not ext:
                                ext = '.jpg'
                            filename = f"image{counter}{ext}"
                            filepath = os.path.join(folder_img, filename)
                            with open(f"{filepath}", "wb") as f:
                                f.write(res_img.content)
                            print(f"Image {filename} sauvegardée.")
                            counter += 1
                except requests.exceptions.RequestException as re:
                    print(f"Impossible de télécharger {url_img}: {re}")

except Exception as e:
    print(f"Une erreur est survenue : {e}")

finally:
    if 'driver' in locals() and driver:
        print("Fermeture du driver")
        driver.quit()