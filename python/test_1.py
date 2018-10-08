import requests
import sys
import bs4
import json

url = 'http://seputu.com/'
headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
response = requests.get(url, headers = headers)
response.encoding = 'UTF-8'
#print(response.text)
soup = bs4.BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8') # html.parser
content = []
for mulu in soup.find_all(class_ = "mulu"):
    h2 = mulu.find('h2')
    if h2 != None:
        h2_title = h2.string # 获取标题
        list = []
        for a in mulu.find(class_ = 'box').find_all('a'):
            href = a.get('href')
            box_title = a.get('title')
            list.append({'href' : href, 'box_title' : box_title})
        content.append({'title' : h2_title, 'content' : list})

with open('cayden.json', 'w', encoding = 'utf-8') as fp:
    fp.write(json.dumps(content))

with open('cayden.json', 'r', encoding = 'utf-8') as fr:
    data = json.loads(fr.read())
    print(data)