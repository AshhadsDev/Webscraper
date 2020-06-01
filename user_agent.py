from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

import csv

f = open('sitemap_cleaned.csv')
csv_f = csv.reader(f)


old_site_class = 'reference'
old_site_domain = 'http://178.128.58.116/index.php'

new_site_class = 'ttref-sup'
new_site_domain = 'https://tobaccotactics.org/wiki'

# duplicate_count = 0
total_count = 0


def extactLink(item):
  try:
    link = item.contents[0].contents[0]
  except IndexError:
    link = None
  return link

with open('write_test.csv', 'w', newline='') as csv_write_file:
  file_writer = csv.writer(csv_write_file, delimiter=',',
                          quotechar=',', quoting=csv.QUOTE_MINIMAL)
  file_writer.writerow(['Url', 'Status', 'Old Site', 'Old Site Unique' 'New Site', 'New Site Unique' 'Match'])
  for row in csv_f:
    total_count += 1
    url = old_site_domain+row[0]
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    try:
      response = urlopen(req)
    except HTTPError as e:
      file_writer.writerow([url, e.code, 0, 0])
    except URLError as e:
      file_writer.writerow([url, e.reason, 0, 0])
    else:
      webpage = response.read()
      soup = BeautifulSoup(webpage, 'html.parser')
      # Get all super scripts
      all_items = soup.find_all('sup', class_=old_site_class)
      # get all anchor link in superscripts
      all_links = map(extactLink, all_items)
      # remove empty sup with no anchor tags
      all_links = list(filter(None, all_links))
      # convert from object to array so we can get count
      all_links_list = list(all_links)

      # Try New Site
      new_url = new_site_domain+row[0]
      new_url = new_url.replace("_", "-")
      new_req = Request(new_url, headers={'User-Agent': 'Mozilla/5.0'})
      try:
        new_response = urlopen(new_req)
      except HTTPError as e:
        file_writer.writerow([new_url, e.code, 0, 0])
      except URLError as e:
        file_writer.writerow([new_url, e.reason, 0, 0])
      else:
        new_webpage = new_response.read()
        new_soup = BeautifulSoup(new_webpage, 'html.parser')
        # Get all super scripts
        new_all_items = new_soup.find_all('sup', class_=new_site_class)
        # get all anchor link in superscripts
        new_all_links = map(extactLink, new_all_items)
        # remove empty sup with no anchor tags
        new_all_links = list(filter(None, new_all_links))
        # convert from object to array so we can get count
        new_all_links_list = list(new_all_links)
        # print(new_url)
        needs_change = 'false'
        if len(all_links_list) == len(new_all_links_list) :
          needs_change = 'true'

        file_writer.writerow([row[0], response.getcode(), len(all_links_list), len(set(all_links_list)), len(new_all_links_list), len(set(new_all_links_list)), needs_change])
        print(row[0])
        print(total_count)
        
      # Debug Logs
      # print(all_links_list)
      # print("count:"+str(len(all_links_list))+", unique:"+str(len(set(all_links_list))))

      # compare list count in original and unique
      # if len(all_links_list) != len(set(all_links_list)):
        # duplicate_count += 1
        # print(url)
  else:
    print('Completed')