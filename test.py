sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'pymodules')))
from googleapiclient.discovery import build
import sys

my_api_key = "AIzaSyARKOEUmrOaeQLrQcbmkz6-q3hghbeA0JY"
my_cse_id = "017294505077652159379:o6a_52asc2u"
num = 5

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

searchStr = ''
toloop = len(sys.argv) - 1
for i in range(0, toloop):
    searchStr = searchStr + sys.argv[i+1] + ' '

results = google_search(
    sys.argv[1], my_api_key, my_cse_id, num=num)

for i in range(0,num):
    print(results[i]['title'] + " Link: " + results[i]['link'])
    
#import os
#import sys
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'pymodules')))
#import requests
#from bs4 import BeautifulSoup

#def web(page):
#    count = len(sys.argv)
#    i = 1
#    searchStr = ''
#    while (count > 1):
#        if searchStr == '':
#            searchStr = sys.argv[i]
#            i = i + 1
#        else:
#            searchStr = searchStr + '+' + sys.argv[i]
#            i = i + 1
#        count = count - 1
#    print(searchStr)
#    url = 'https://check4spam.com/?s=' + searchStr
#    if(page>0):
#        code = requests.get(url)
#        plain = code.text
#        s = BeautifulSoup(plain, "html.parser")
        #print(s.find_all('a'))
#        for link in s.findAll('a', {'class':'post-title'}):
            #print(link.get_text())
            #tet = link.get('title')
            #print(tet)
#            tet_2 = link.get('href')
#            print(tet_2)
#web(1)