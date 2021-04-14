import requests
from bs4 import BeautifulSoup
import urllib.request


def download_images(start, end, url, out):
    for i in range(start, end + 1):
        try:
            urllib.request.urlretrieve(url + f"{i}.jpg", f"{out}{i}.jpg")
        except Exception as e:
            print(f"{i} : {e}")


def main():
    download_images(756327813, 756400219, "https://lunappimg.appspot.com/lun-ua/828/672/images-cropped/", "images/")


if __name__ == '__main__':
    main()

