import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, "lxml")

# Title
title = soup.find("h1").text.strip()

# Price
price = soup.select_one(".price_color").text.strip()

# Rating
rating = soup.select_one("p.star-rating")["class"][1]

# Availability
availability = soup.select_one(".availability").text.strip()

# Category (breadcrumb)
category = soup.select("ul.breadcrumb li a")[2].text.strip()

print({
    "title": title,
    "price": price,
    "rating": rating,
    "availability": availability,
    "category": category
})
