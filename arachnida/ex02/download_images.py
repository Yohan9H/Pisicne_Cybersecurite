import urllib.request
import os

IMAGES_TO_DOWNLOAD = {
    "test_exif.jpg": "https://raw.githubusercontent.com/ianare/exif-samples/master/jpg/Canon_40D.jpg",
    "test.png": "https://raw.githubusercontent.com/python-pillow/Pillow/main/Tests/images/hopper.png",
    "test.gif": "https://raw.githubusercontent.com/python-pillow/Pillow/main/Tests/images/hopper.gif",
    "test.bmp": "https://raw.githubusercontent.com/python-pillow/Pillow/main/Tests/images/hopper.bmp"
}

def download_test_images():
    print("Vérification et téléchargement des images de test...")
    for filename, url in IMAGES_TO_DOWNLOAD.items():
        if not os.path.exists(filename):
            try:
                print(f"Téléchargement de {filename}...")
                urllib.request.urlretrieve(url, filename)
                print(f"-> {filename} téléchargé avec succès.")
            except Exception as e:
                print(f"ERREUR: Impossible de télécharger {filename}. Raison: {e}")
        else:
            print(f"-> {filename} existe déjà, pas de téléchargement.")
    print("\nVérification terminée.")

if __name__ == "__main__":
    download_test_images()
