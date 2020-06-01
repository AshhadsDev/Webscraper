import requests
import re
from bs4 import BeautifulSoup as soup
r = requests.get('https://tobaccotactics.org/wiki/e-cigarettes-imperial-tobacco/', proxies={'http':'50.207.31.221:80'}).text
results = re.findall('Revenue of \$[a-zA-Z0-9\.]+', r)
print(r)