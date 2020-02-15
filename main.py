# coding=utf-8
import requests
import json
from lxml import html
# payload = {'page': '2', 'regular-txt': '', 'regular-case_doc': '', 'regular-lawchunkinfo': 'Статья 156. Неисполнение обязанностей по воспитанию несовершеннолетнего(УК РФ)', 'regular-date_from': '01.02.2009', 'regular-date_to': '11.02.2020', 'regular-workflow_stage': '', 'regular-area': '1013', 'regular-court': '', 'regular-judge': '', '_': '1581376199542'}
payload = {'regular-txt': '', 'regular-case_doc': '', 'regular-lawchunkinfo': 'Статья 156. Неисполнение обязанностей по воспитанию несовершеннолетнего(УК РФ)', 'regular-date_from': '01.02.2009', 'regular-date_to': '11.02.2020', 'regular-workflow_stage': '', 'regular-area': '1013', 'regular-court': '', 'regular-judge': '', '_': '1581376199542'}
# doc/iuOPoETzGvg8
#url = 'https://sudact.ru/regular/doc_ajax/'
url = 'https://sudact.ru/regular/doc/iuOPoETzGvg8/'
r = requests.get(url, verify=False, params=payload)
print r
txt = ''
with open('test.html', 'w') as output_file:
  output_file.write(r.text.encode('utf-8'))
  txt += r.text.encode('utf-8')

ptxt = json.loads(txt)
#cptxt = ptxt['content']
#cptxt = '<html><head></head><body>' + cptxt + '</body></html>'
print cptxt
tree = html.fromstring(cptxt)
res = tree.xpath('//a/@text()')
print res
# res = tree.xpath('//a/@href') # все h2 теги
# print res[0]
# for i in range(len(res)):
#     print res[i]

#soup = BeautifulSoup(cptxt)
#film_list = soup.find('a', {'class': 'bookmarkIcon'})
#print film_list