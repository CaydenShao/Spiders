# coding:utf-8
from urllib import request
from urllib import parse
from urllib import response

def download(url, user_agent = 'wswp', num_retries = 2):
    print('Downloading:' + url)
    headers = {'User-agent' : user_agent}
    req = request.Request(url, headers = headers)
    try:
        html = request.urlopen(req).read()
    except request.URLError as e:
        print ('Download error:' + e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code and e.code < 600:
                # retry 5XX HTTP errors
                return download(url, user_agent, num_retries - 1)
    return html

if __name__ == '__main__':
    html = download('http://www.baidu.com')
    print(html)