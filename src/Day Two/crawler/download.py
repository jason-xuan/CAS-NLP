# -*- coding: utf-8 -*-
# @Author: jason-xuan
# @Date:   2017-08-07 09:33:12
# @Last Modified by:   jason-xuan
# @Last Modified time: 2017-08-07 11:25:45
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


if not os.path.exists('./Download'):
    os.mkdir('./Download')


def download(urls):
    # 重用 TCP
    sess = requests.Session()

    failed_list = []

    for url in tqdm(urls):
        try:
            r = sess.get(url)
            r.encoding = 'gbk'
            soup = BeautifulSoup(r.text, 'lxml')

            title = soup.find('div', 'article_area').find('h1').string
            title = title.replace('"', '').replace('/', '').replace('\\', '')
            texts = [''.join(s.strings) for s in soup.find('div', 'article_area').find_all('p')]
            text = '\n'.join(texts).replace('\u3000', '')
            with open('Download/{0}.txt'.format(title), 'w', encoding='utf-8') as f:
                f.write(text)

        except BaseException as e:
            # print("url:{0} parse failed..".format(url))
            print(e)
            failed_list.append(url)

    print('{0} failed download'.format(len(failed_list)))

    with open('failed urls.txt', 'w') as f:
        f.write('\n'.join(failed_list))

    return len(failed_list)

def first_download():
    # read the file
    with open('SogouTDTE.txt', 'r') as f:
        lines = [line.split('\t') for line in f.read().split('\n')][:-1]

    urls = [url for url, _ in lines]

    return download(urls)


def re_download():
    # read the file
    with open('failed urls.txt', 'r') as f:
        lines = [line for line in f.read().split('\n')]

    return download(lines)

# for _ in range(10):
#     re_download()

if __name__ == '__main__':
    last = first_download()

    current = re_download()

    # 重复洗失效链接直到两次爬取失效链接数相同为止
    while current != last:
        last = current
        current = re_download()
