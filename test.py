#import sys
#print('testt2', sys.argv[1]);
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'pymodules')))
import requests
from bs4 import BeautifulSoup

def web(page):
    count = len(sys.argv)
    i = 1
    searchStr = ''
    while (count > 1):
        if searchStr == '':
            searchStr = sys.argv[i]
            i = i + 1
        else:
            searchStr = searchStr + '+' + sys.argv[i]
            i = i + 1
        count = count - 1
    print(searchStr)
    url = 'https://check4spam.com/?s=' + searchStr
    if(page>0):
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        #print(s.find_all('a'))
        for link in s.findAll('a', {'class':'post-title'}):
            #print(link.get_text())
            #tet = link.get('title')
            #print(tet)
            tet_2 = link.get('href')
            print(tet_2)
web(1)