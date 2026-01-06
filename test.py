import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, "lxml")

# Récupération de l'image
img_tag = soup.select_one(".item.active img")
#img_src = img_tag["src"]

# Construire l'URL absolue
img_url = urljoin(url, img_tag["src"])

print(img_url)
