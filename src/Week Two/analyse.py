# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 00:07:09 2017

@author: zjxua
"""
import math
import numpy as np
from functools import reduce
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


def tfidf() -> list:
    # 所有doc的列表
    docs = Doc.get_processed()
    # TF
    #   计算每个文档的各个词的词频
    for doc in docs:
        doc.word_freq = {}
        for word in doc.word_list:
            if word not in doc.word_freq:
                doc.word_freq[word] = 1
            else:
                doc.word_freq[word] += 1

    # 计算tf值
    for doc in docs:
        doc.tf = {}
        doc_len = len(doc.word_list)
        for word in doc.word_set:
            doc.tf[word] = doc.word_freq[word] / doc_len

    # for doc in docs:
    #     pprint(doc.word_freq)

    # IDF
    #   建立 词 - doc 的词频矩阵 dense
    #   用于计算逆文档频率
    # 全部词列表
    all_word = list(reduce(lambda x, y: x | y, [doc.word_set for doc in docs]))
    # idf {
    #   word: idf value
    # }
    idf = {}
    len_docs = len(docs)
    for word in all_word:
        # idf[word] =
        word_count = 1
        for doc in docs:
            if word in doc.word_set:
                word_count += 1
                # idf[word][doc.docno] = doc.word_freq[word]
            # else:
            #     idf[word][doc.docno] = 0
        # 相当于word_count + 1，避免分母为0
        idf[word] = math.log(len_docs / word_count)

    # pprint(idf)

    # 计算每个文档里每个词的 TFIDF值
    for doc in docs:
        doc.tfidf = {}
        for word in doc.word_set:
            doc.tfidf[word] = doc.tf[word] * idf[word]

    for doc in docs:
        items = list(doc.tfidf.items())
        items.sort(key=lambda x: x[1], reverse=True)

        # pprint(items[:10])

    # 找top-10, 将每个doc的top-10词设为一个集合，计算每个doc对于这个集合的词频矩阵

        doc.top_10 = [p[0] for p in items[:10]]
        # pprint(doc.top_10)

    high_freq_set = set(reduce(lambda x, y: x + y, [doc.top_10 for doc in docs]))
    high_freq_list = list(high_freq_set)

    for doc in docs:
        doc.vec = np.zeros( (len(high_freq_list),))
        for i in range(len(high_freq_list)):
            word = high_freq_list[i]
            doc.vec[i] = doc.tf[word] if word in doc.tf else 0

        # pprint(doc.vec)

    vectors = [doc.vec for doc in docs]

    return vectors

if __name__ == '__main__':
    pprint(tfidf())
