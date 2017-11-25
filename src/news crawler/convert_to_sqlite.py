# -*- coding: utf-8 -*-
# @Author: jason-xuan
# @Date:   2017-08-09 11:34:48
# @Last Modified by:   jason-xuan
# @Last Modified time: 2017-08-20 01:29:10
from doc_pb2 import Document
from tqdm import tqdm
from os import path
import json


def read_line(file_path):
    with open(file_path, 'rb') as f:
        for line in f:
            yield line


def save_json(out_file, texts):
    for t in tqdm(texts):
        json_object = json.loads(t)
        doc = Document()

        doc.url = json_object['url']
        doc.source = json_object['source']
        doc.title = json_object['title'].replace('\n', '')
        doc.content = json_object['text'].replace('\n', '')

        out_file.write(doc.SerializeToString())
        out_file.write(bytes('\n', encoding='utf-8'))



def save_as_protobuf(out_path=r'./sina_products.proto', file_path=r'news_tensite_xml.dat', \
        read_method=read_line, save_method=save_json):

        texts = read_method(file_path)
        with open(out_path, 'wb') as f:
            save_method(f, texts)


if __name__ == '__main__':
    save_as_protobuf(r'./sina_2017-08-19_products.buf', r'./sina_2017-08-19_products.json', read_line, save_json)
