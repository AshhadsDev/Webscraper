import re
import csv
from bs4 import BeautifulSoup


text = "In the UK and the US most right-wing and libertarian think tanks do not disclose who funds them, so the link to the tobacco industry, if it exists, is often hidden. The millions of tobacco industry documents in the <ref name='bl'>Legacy</ref> Tobacco Documents Library do show that certain leading right wing UK think tanks such as the [[Adam Smith Institute]] and the [[Institute of Economic Affairs]] used to receive tobacco funding. While the IEA does not disclose its funding sources and has repeatedly received a “one star” (the lowest) rating by transparency watchdog Transparency International <ref>Transparify, [https://web.archive.org/web/20190103153936/https:/www.transparify.org/blog/2018/11/16/pressure-grows-on-uk-think-tanks-that-fail-to-disclose-their-funders Pressure grows on UK think tanks that fail to disclose their funders], 16 November 2018, accessed July 2019</ref> it is known to have received funding from British American Tobacco (BAT) since 1963, and to date (January 2019) BAT describes itself as an IEA member in the EU Transparency Register.<ref> EU Transparency Register, [https://web.archive.org/save/http:/ec.europa.eu/transparencyregister/public/consultation/displaylobbyist.do?id=2427500988-58 British American Tobacco], last modified 23 May 2018, accessed January 2019</ref> As can be seen in the list below, such a lack of transparency is not limited to the UK."
# words = text.partition("")
# words = text.partition("<ref>(.+?)</ref>")
# words = text.partition("^<ref></ref>$")
# words = text.partition('<ref[^>]*>([^<]+)</ref>')
# words = text.partition('^<ref>(.*?)</ref>$')
# words = text.partition('<ref>(.*?)</ref>')
# words = text.partition('<ref>Legacy</ref>')
# words = text.partition('<ref>(.*)</ref>')
# words = text.partition('<ref>.*?</ref>')
# words = text.partition('</ref>$')
# words = text.partition('cco$')

# x = re.search("^US.*libertarian$", text)
# x = re.search("<ref(.+?)</ref>", text)
# if x :
# 	print(x.span())
# 	print('----')
# 	print(x.string)
# 	print('----')
# 	print(x.group())	
# else:
# 	print('-- not found --')


with open('old_ref_words.csv', 'w', newline='') as csv_write_file:
  file_writer = csv.writer(csv_write_file, delimiter=',',
                          quotechar='"', quoting=csv.QUOTE_MINIMAL)
  file_writer.writerow(['start_words', 'end_words', 'words_hash', "ref_text", 'ref_name'])

  for match in re.finditer("<ref(.+?)</ref>", text):
    s = match.start() #position the ref starts
    e = match.end() #position the ref ends

    # Get the two words before the ref tag
    firstwords = text[0:s].split()[-2:]

    # Get the two words after the ref tag
    lastwords = text[e:].split()[:2]

    wordhash = ' '.join(firstwords)+' '+' '.join(lastwords)

    print(text[s:e])

    ref_name = 'none'
    # Extact the name attribute
    if(re.search("name=", text[s:e])):
      soup = BeautifulSoup(text[s:e], 'html.parser')
      ref_name = soup.ref['name']

    file_writer.writerow([' '.join(firstwords), ' '.join(lastwords), wordhash, text[s:e], ref_name])



    # print('String match "%s" at %d:%d' % (text[s:e], s, e))

# words = text.partition('<ref>Transparify, [https://web.archive.org/web/20190103153936/https:/www.transparify.org/blog/2018/11/16/pressure-grows-on-uk-think-tanks-that-fail-to-disclose-their-funders Pressure grows on UK think tanks that fail to disclose their funders], 16 November 2018, accessed July 2019</ref>')
# print(words[0])
# print('---------------')
# print(words[1])
# print('---------------')
# print(words[2])
