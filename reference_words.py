from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re
import csv

# f = open('sitemap_cleaned.csv')
# csv_f = csv.reader(f)


# old_site_class = 'reference'
url = 'http://178.128.58.116/index.php?title=Think_Tanks&action=edit'

# new_site_class = 'ttref-sup'
# new_site_domain = 'https://tobaccotactics.org/wiki'

# duplicate_count = 0
# total_count = 0


# def extactLink(item):
#   try:
#     link = item.contents[0].contents[0]
#   except IndexError:
#     link = None
#   return link

# with open('write_test.csv', 'w', newline='') as csv_write_file:
#   file_writer = csv.writer(csv_write_file, delimiter=',',
#                           quotechar=',', quoting=csv.QUOTE_MINIMAL)
#   file_writer.writerow(['Url', 'Status', 'Old Site', 'Old Site Unique' 'New Site', 'New Site Unique' 'Match'])
  # for row in csv_f:
    # total_count += 1
    # url = old_site_domain+row[0]
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
  response = urlopen(req)
except HTTPError as e:
  print(e.code)
except URLError as e:
  print(e.reason)
else:
  webpage = response.read()
  soup = BeautifulSoup(webpage, 'html.parser')
  text_markup = soup.find('textarea', id='wpTextbox1')
  # print(text_markup.contents[0].string) 
  text = text_markup.contents[0].string

  with open('reference_words.csv', 'w', newline='') as csv_write_file:
    file_writer = csv.writer(csv_write_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['start_words', 'end_words', 'words_hash', "ref_text", 'ref_name'])

    # Counts
    t = 0

    for match in re.finditer("<ref(.+?)</ref>", text):
      t += 1
      s = match.start() #position the ref starts
      e = match.end() #position the ref ends

      # Get the two words before the ref tag
      firstwords = text[0:s].split()[-2:]

      # Get the two words after the ref tag
      lastwords = text[e:].split()[:2]

      wordhash = ' '.join(firstwords)+' '+' '.join(lastwords)

      print(text[s:e])

      ref_name = 'empty'
      ref_string = text[s:e]
      # Extact the name attribute
      if(re.search("name\s?=", ref_string)):

        if len(ref_string) >= 1:
          # Remove extra spaces
          ref_markup = BeautifulSoup(ref_string, 'html.parser')

          ref_name = ref_markup.ref['name']
          if len(ref_name) >= 1:
            # Remvoe slash
            ref_name = ref_name.replace('/', '')

      # Write to csv if reference name exists
      if ref_name != 'empty' :
        file_writer.writerow([' '.join(firstwords), ' '.join(lastwords), wordhash, text[s:e], ref_name])

      # Write to csv - all reference
      # file_writer.writerow([' '.join(firstwords), ' '.join(lastwords), wordhash, text[s:e], ref_name])
