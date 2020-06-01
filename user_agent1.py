from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

import csv

f = open('sitemap_limited.csv')
csv_f = csv.reader(f)

old_site_class = 'reference'
new_site_class = 'ttref-sup'
duplicate_count = 0
total_count = 0

def extactLink(item):
  try:
    link = item.contents[0].contents[0]
  except IndexError:
    link = None
  return link

for row in csv_f:
  url = 'https://tobaccotactics.org/wiki'+row[0]
  req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  try:
    response = urlopen(req)
  except HTTPError as e:
    print('Error code: ', e.code)
  except URLError as e:
    print('Reason: ', e.reason)
  else:
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    # Get all super scripts
    all_items = soup.find_all('sup', class_=new_site_class)

    # get all anchor link in superscripts
    all_links = map(extactLink, all_items)
    all_links = list(filter(None, all_links))

    print(all_links)
    # convert from object to array so we can get count
    all_links_list = list(all_links)

    total_count += 1
    # Debug Logs
    print(all_links_list)
    print("count:"+str(len(all_links_list))+", unique:"+str(len(set(all_links_list))))

    # compare list count in original and unique
    if len(all_links_list) != len(set(all_links_list)):
      duplicate_count += 1
      print(url)
      print(len(all_links_list))
else:
  print('Checked: '+str(total_count))
  print('Duplaces: '+str(duplicate_count))