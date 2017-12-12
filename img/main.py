# coing: utf-8
import re
import requests
import urllib.parse
from bs4 import BeautifulSoup
import threading
import queue
import time
import sys


INIT_URL = "http://www.27270.com/ent/meinvtupian/"
pageset = set()
count = 0
cache = queue.Queue(0)
imgset = set()
urlheader = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Host': "t2.hddhhn.com",
    'Proxy-Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-SG,zh;q=0.9,zh-CN;q=0.8,en;q=0.7,zh-TW;q=0.6'
}
imgheader = urlheader


def parse_page(url):
    global count, pageset, imgset
    base_url = urllib.parse.urlparse(url).netloc
    urlheader['Host'] = base_url
    try:
        context = requests.get(url, headers=urlheader, timeout=3).content.decode('utf-8', 'ignore')
    except:
        return
    soup = BeautifulSoup(context, 'lxml')
    for line in soup.find_all('img', src=re.compile("http://.+\.(jpg|png|jpeg)$"), width=True, height=True):
        width = int(line.get('width'))
        height = int(line.get('height'))
        src = line.get('src')
        if width > 150 and height > 150:
            if src not in imgset:
                cache.put([url, src])
                imgset.add(src)
    for line in soup.find_all('a', href=re.compile("http://www.27270.com/ent/meinvtupian/.+")):
        href = line.get('href')
        if href not in pageset:
            pageset.add(href)
            parse_page(href)


def save_img():
    while True:
        global count
        [url, src] = cache.get()
        imgheader['Referer'] = url
        imgheader['Host'] = urllib.parse.urlparse(src).netloc
        try:
            img = requests.get(src, headers=imgheader, timeout=3).content
        except:
            continue
        count = count + 1
        if count > 15000:
            sys.exit("crawler done!")
        imgset.add(src)
        print(str(src))
        with open(str(count) + '.jpg', 'wb') as f:
            f.write(img)


thread_parse = threading.Thread(target=parse_page, name="parse", args=(INIT_URL,))
thread_parse.start()
thread_save = threading.Thread(target=save_img, name="save")
thread_save.start()
thread_parse.join()
thread_save.join()
