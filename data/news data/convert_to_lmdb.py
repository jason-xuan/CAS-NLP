# -*- coding: utf-8 -*-
# @Author: jason-xuan
# @Date:   2017-08-09 11:34:48
# @Last Modified by:   jason-xuan
# @Last Modified time: 2017-08-09 13:20:19
from doc_pb2 import Document
from bs4 import BeautifulSoup
from tqdm import tqdm
from pprint import pprint
import lmdb
import json


def read_xml(file_path):
    print('loading news_tensite_xml.dat, nearly cost 12s')
    with open(file_path, 'r', encoding='GB18030') as f:
        text = f.read()

    texts = [s + '</doc>' for s in text.split('</doc>') if s != '']

    return texts


def save_xml(db, texts):
    with db.begin(write=True) as txn:
        for t in tqdm(texts):
            try:
                soup = BeautifulSoup(t, 'xml')
                doc = Document()

                docno = soup.find('docno')
                if docno:
                    # soup.find('docno') => <docno/>
                    doc.docno = docno.string if docno.string is not None else ''
                else:
                    doc.docno = ''

                url = soup.find('url')
                if url:
                    # soup.find('url') => <url/>
                    doc.url = url.string if url.string is not None else ''
                else:
                    doc.url = ''

                title = soup.find('contenttitle')
                if title:
                    # soup.find('contenttitle') => <<contenttitle/>/>
                    doc.content = title.string if title.string is not None else ''
                else:
                    doc.title = ''

                content = soup.find('content')
                if content:
                    # soup.find('content') => <content/>
                    doc.content = content.string if content.string is not None else ''
                else:
                    doc.content = ''

                if doc.title != '' or doc.content != '':
                    txn.put(bytes(doc.url, 'utf-8'), doc.SerializeToString())

            except BaseException as e:
                print(soup)
                raise e


def read_line(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line


def save_json(db, texts):
    with db.begin(write=True) as txn:
        for t in tqdm(texts):
            try:
                json_object = json.loads(t)
                doc = Document()

                doc.url = json_object['url']

                doc.source = json_object['source']

                doc.title = json_object['title']

                doc.content = json_object['text']

                txn.put(bytes(doc.url, 'utf-8'), doc.SerializeToString())

            except BaseException as e:
                print(soup)
                raise e


def save_to_lmdb(lmdb_path=r'./documents', file_path=r'news_tensite_xml.dat', \
        read_method=read_xml, save_method=save_xml):

    print('creating lmdb database documents, size set to nearly 10GB')
    db = lmdb.open(lmdb_path, writemap=True, map_size=10000000000)
    texts = read_method(file_path)
    save_method(db, texts)
    pprint(db.stat())


if __name__ == '__main__':
    save_to_lmdb(r'./documents', r'./sina_products.json', read_line, save_json)
