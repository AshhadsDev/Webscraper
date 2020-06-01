import csv

f = open('sitemap_limited.csv')
csv_f = csv.reader(f)

for row in csv_f:
  print(row)