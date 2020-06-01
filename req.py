from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# url = "https://stopttdev.wpengine.com/wiki/aaron-sherinian-d74/"
url = "https://tobaccotactics.org/wiki/Heated_Tobacco_Products"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
  response = urlopen(req)
except HTTPError as e:
  print('Error code: ', e.code)
except URLError as e:
  print('Reason: ', e.reason)
else:
  print('good!')