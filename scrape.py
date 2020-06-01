import requests
from bs4 import BeautifulSoup

# page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
page = requests.get("https://stopttdev.wpengine.com/wiki/aaron-sherinian-d74/")
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')
# all_items = soup.find_all('p')
# print(all_items)