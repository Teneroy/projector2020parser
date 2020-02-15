# coding=utf-8
import requests
import json
from lxml import html

def findInArr(array, value):
    for i in range(len(array)):
        if array[i] == value:
            return True
    return False

def find(array, set):
    listval = []
    for i in range(len(array)):
        if findInArr(set, array[i]):
            listval.append(array[i])
            #return True
    if len(listval) != 0:
        return listval, True
    return listval, False

def filterData(data, result):
    for i in range(len(data)):
        print data[i]
        string_to_list = data[i].encode('utf-8').split()
        if len(string_to_list) == 3:  # пока так, потом придумать более надежный
            if string_to_list[1] == 'УК' and string_to_list[2] == 'РФ':
                result.append(string_to_list[0])

def findValuesPage(text, value, set, tree):
    res = tree.xpath('//a/text()')
    filtered = []
    filterData(res, filtered)
    print filtered
    return find(filtered, set)

def findHeader(tree):
    res = tree.xpath('//h1/text()')
    return res[0]

# payload = {'page': '2', 'regular-txt': '', 'regular-case_doc': '', 'regular-lawchunkinfo': 'Статья 156. Неисполнение обязанностей по воспитанию несовершеннолетнего(УК РФ)', 'regular-date_from': '01.02.2009', 'regular-date_to': '11.02.2020', 'regular-workflow_stage': '', 'regular-area': '1013', 'regular-court': '', 'regular-judge': '', '_': '1581376199542'}
pagereq = {'regular-txt': '', 'regular-case_doc': '',
           'regular-lawchunkinfo': 'Статья 156. Неисполнение обязанностей по воспитанию несовершеннолетнего(УК РФ)',
           'regular-date_from': '01.02.2009', 'regular-date_to': '11.02.2020', 'regular-workflow_stage': '',
           'regular-area': '1013', 'regular-court': '', 'regular-judge': '', '_': '1581376199542'}
# doc/iuOPoETzGvg8
# url = 'https://sudact.ru/regular/doc_ajax/'
page_id = 'dUxZAyhVAylC'
url = 'https://sudact.ru/regular/doc/' + page_id + '/'
r = requests.get(url, verify=False, params=pagereq)
print r
txt = r.text.encode('utf-8')
tr = html.fromstring(txt)
array_vals, found = findValuesPage(txt, '156', ['117', '116', '125', '161'], tr)
if found:
    array_vals = list(dict.fromkeys(array_vals))
    print array_vals
print findHeader(tr)
# ptxt = json.loads(txt)
# cptxt = ptxt['content']
# cptxt = '<html><head></head><body>' + cptxt + '</body></html>'
# print cptxt
# tree = html.fromstring(cptxt)
# res = tree.xpath('//a/@text()')
# print res
# res = tree.xpath('//a/@href') # все h2 теги
# print res[0]
# for i in range(len(res)):
#     print res[i]

# soup = BeautifulSoup(cptxt)
# film_list = soup.find('a', {'class': 'bookmarkIcon'})
# print film_list
