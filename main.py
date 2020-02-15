# coding=utf-8
import requests
import json
from lxml import html
import xlsxwriter

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
        #print data[i]
        string_to_list = data[i].encode('utf-8').split()
        if len(string_to_list) == 3:  # пока так, потом придумать более надежный
            if string_to_list[1] == 'УК' and string_to_list[2] == 'РФ':
                result.append(string_to_list[0])

def filterLinks(data, result):
    for i in range(len(data)):
        string_to_list = data[i]['text'].encode('utf-8').split()
        if string_to_list[0] == 'Приговор':
            result.append(data[i])

def findValuesPage(text, value, set, tree):
    res = tree.xpath('//a/text()')
    filtered = []
    filterData(res, filtered)
    #print filtered
    return find(filtered, set)

def findHeader(tree):
    res = tree.xpath('//h1/text()')
    return res[0]

def printLinks(data):
    for i in range(len(data)):
        print data[i]['text']
       #print data[i]['link']

def merge(arr1, arr2, attr1, attr2):
    merged = []
    for i in range(len(arr1)):
        merged.append({attr1: arr1[i], attr2: arr2[i]})
    return merged

def writeArr(arr, rw, cl, wsh):
    for i in range(len(arr)):
        wsh.write(rw, cl, arr[i])
        cl += 1
    wsh.write(rw, cl, '156')

def parsePages(pages, preq, wsh):
    for i in range(len(pages)):
        page_id = pages[i]['link'].split('/')[3]
        url = 'https://sudact.ru/regular/doc/' + page_id + '/'
        r = requests.get(url, verify=False, params=pagereq)
        print r
        txt = r.text.encode('utf-8')
        tr = html.fromstring(txt)
        array_vals, found = findValuesPage(txt, '156', ['117', '116', '125'], tr)
        if found:
            array_vals = list(dict.fromkeys(array_vals))
            print array_vals
            global g_rw
            g_rw += 1
            wsh.write(g_rw, 1, findHeader(tr))
            wsh.write(g_rw, 2, url)
            writeArr(array_vals, g_rw, 3, wsh)

g_rw = 0
pagefrom = 0
pagecount = 13
workbook = xlsxwriter.Workbook('Expenses' + str(pagefrom) + '.xlsx')
worksheet = workbook.add_worksheet()

pagereq = {'regular-txt': '', 'regular-case_doc': '',
           'regular-lawchunkinfo': 'Статья 156. Неисполнение обязанностей по воспитанию несовершеннолетнего(УК РФ)',
           'regular-date_from': '01.02.2009', 'regular-date_to': '11.02.2020', 'regular-workflow_stage': '',
           'regular-area': '1013', 'regular-court': '', 'regular-judge': '', '_': '1581376199542'}


for i in range(pagefrom, pagecount):
    payload = {'page': i, 'regular-txt': '', 'regular-case_doc': '', 'regular-lawchunkinfo': 'Статья 156. Неисполнение обязанностей по воспитанию несовершеннолетнего(УК РФ)', 'regular-date_from': '01.02.2009', 'regular-date_to': '11.02.2020', 'regular-workflow_stage': '10', 'regular-area': '', 'regular-court': '', 'regular-judge': '', '_': '1581376199542'}
    listurl = 'https://sudact.ru/regular/doc_ajax/'
    listr = requests.get(listurl, verify=False, params=payload)
    print "page: ", i
    print listr
    listtxt = listr.text.encode('utf-8')
    if listtxt[0] == '<' and listtxt[1] == '!':
        workbook.close()
    ptxt = json.loads(listtxt)
    cptxt = ptxt['content']
    cptxt = '<html><head></head><body>' + cptxt + '</body></html>'
    listtr = html.fromstring(cptxt)
    listres_links = listtr.xpath('//a/@href')
    listres_text = listtr.xpath('//a/text()')
    listres = merge(listres_links, listres_text, "link", "text")
    #print listres
    filteredlinks = []
    filterLinks(listres, filteredlinks)
    printLinks(filteredlinks)
    parsePages(filteredlinks, pagereq, worksheet)



# doc/iuOPoETzGvg8
# url = 'https://sudact.ru/regular/doc_ajax/'
# page_id = 'dUxZAyhVAylC'
# url = 'https://sudact.ru/regular/doc/' + page_id + '/'
# r = requests.get(url, verify=False, params=pagereq)
# print r
# txt = r.text.encode('utf-8')
# tr = html.fromstring(txt)
# array_vals, found = findValuesPage(txt, '156', ['117', '116', '125', '161'], tr)
# if found:
#     array_vals = list(dict.fromkeys(array_vals))
#     print array_vals
# print findHeader(tr)

#worksheet.write(0,0,array_vals[0])
workbook.close()

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
