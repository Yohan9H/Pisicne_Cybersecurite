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

def download_images_from_page(driver, page_url, folder_path):
    wait = WebDriverWait(driver, 10)
    simple_for_print = urllib.parse.urlparse(page_url).path
    print(f"Recherche d'images sur : {simple_for_print}")

    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"{len(images)} images trouvées ! Téléchargement en cours :")

        os.makedirs(folder_path, exist_ok=True)
        image_count = 1

        page_path_prefix = urllib.parse.urlparse(page_url).path
        if page_path_prefix.startswith('/'):
            page_path_prefix = page_path_prefix[1:]
        page_path_prefix = page_path_prefix.replace('/', '_').replace('.', '_')
        if not page_path_prefix:
            page_path_prefix = "page"

        for img_tag in images:
            img_src = img_tag.get_attribute('src')
            if not img_src:
                continue
            
            url_img = urllib.parse.urljoin(page_url, img_src)

            if url_img.lower().startswith('http'):
                try:
                    path = urllib.parse.urlparse(url_img).path
                    if path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                        res_img = requests.get(url_img, timeout=10)
                        if res_img.status_code == 200:
                            ext = os.path.splitext(path)[1]
                            if not ext: ext = '.jpg'
                            
                            filename = f"{page_path_prefix}_image{image_count}{ext}"
                            filepath = os.path.join(folder_path, filename)
                            with open(filepath, "wb") as f:
                                f.write(res_img.content)
                                print(filename, "téléchargée")
                            image_count += 1
                except requests.exceptions.RequestException as re:
                    print(f"Impossible de télécharger {url_img}: {re}")
    except Exception as e:
        print(f"Aucune image trouvée ou erreur durant le scraping de {simple_for_print}: {e}")


def find_pages(driver, current_url) -> set:
    url_base = urllib.parse.urlparse(url_web).netloc
    pages_found_elements = driver.find_elements(By.TAG_NAME, "a")

    pages_filter = set()
    for link_element in pages_found_elements:
        href = link_element.get_attribute('href')
        if href:
            url_complete = urllib.parse.urljoin(current_url, href)
            domaine_lien_found = urllib.parse.urlparse(url_complete).netloc
            if domaine_lien_found == url_base and url_complete.startswith('http'):
                pages_filter.add(url_complete)
    return pages_filter



try:
    driver = webdriver.Chrome(options=chrome_options)
    print("Driver initialisé.")

    if recursif is True:
        print(f"Lancement du scraping récursif avec une profondeur de {len_rec}.")
        
        list_pages = [(url_web, 0)]
        list_pages_visited = {url_web}
        
        while list_pages:
            current_url, current_depth = list_pages.pop(0)
            print(f"Visite de : {current_url} (Profondeur {current_depth})" )
            try:
                driver.get(current_url)
                download_images_from_page(driver, current_url, folder_img)
                
                if current_depth < len_rec:
                    new_links = find_pages(driver, current_url)
                    for link in new_links:
                        if link not in list_pages_visited:
                            list_pages_visited.add(link)
                            list_pages.append((link, current_depth + 1))
            except Exception as page_error:
                print(f"Impossible de traiter la page {current_url}: {page_error}")
    else:
        driver.get(url_web)
        print(f"Site : {driver.title}")
        download_images_from_page(driver, url_web, folder_img)

except Exception as e:
    print(f"Une erreur majeure est survenue : {e}")

finally:
    if 'driver' in locals() and driver:
        print("Fermeture du driver")
        driver.quit()
