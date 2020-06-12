from bs4 import BeautifulSoup

txt = "documents in the <ref name='bl'>Legacy</ref> Tobacco Documents"
soup = BeautifulSoup(txt, 'html.parser')

print(soup.ref['name'])

