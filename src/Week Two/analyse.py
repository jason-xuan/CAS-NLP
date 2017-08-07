# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 00:07:09 2017

@author: zjxua
"""
from pprint import pprint
from reader import Doc


def analyse():
    processed = Doc.get_processed()
    doc_docnos = [doc.docno for doc in processed]
    result = {}
    for doc in processed:
        for word in doc.word_list:
            if word not in result:
                result[word] = {docno: 0 for docno in doc_docnos}
            result[word][doc.docno] += 1
    with open('result.txt', 'w') as out:
        pprint(result, stream=out)


