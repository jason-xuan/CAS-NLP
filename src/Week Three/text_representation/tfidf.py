from gensim import corpora, models, similarities
from pprint import pprint
from os import path
import jieba
import numpy as np
import heapq
import pickle
import logging


from .reader import get_sentences, read_titles


def build_model():
    sentences = get_sentences()

    words_split = [sentence.split(' ') for sentence in sentences]

    # remove words that appear only once
    from collections import defaultdict

    frequency = defaultdict(int)
    for text in words_split:
        for token in text:
            frequency[token] += 1

    words_split = [[token for token in text if frequency[token] > 1] for text in words_split]

    dictionary = corpora.Dictionary(words_split)
    corpus = [dictionary.doc2bow(text) for text in words_split]

    model = models.TfidfModel(corpus)
    feature_num = len(dictionary.token2id.keys())
    index = similarities.SparseMatrixSimilarity(model[corpus], num_features=feature_num)

    return dictionary, index, model


def nlargest(array: np.ndarray, n: int) -> list:
    return heapq.nlargest(n, range(len(array)), array.take)


def tfidf_process():
    videotitles = read_titles()
    if not path.isfile(r'./temp/model.pickle'):
        logging.info('model.pickle not found, rebuilding...')
        dictionary, index, model = build_model()
        with open(r'./temp/model.pickle', 'wb') as f:
            pickle.dump((dictionary, index, model), f)
    else:
        logging.info('model.pickle found, loading...')
        with open(r'./temp/model.pickle', 'rb') as f:
            dictionary, index, model = pickle.load(f)


    while True:
        print('Type "EXIT to exit"')
        new_doc = input('type videl title: ')
        exist = False
        if new_doc == "EXIT":
            break
        if new_doc in videotitles:
            exist = True
        # new_doc = '韩国最帅面孔'
        new_vec = dictionary.doc2bow([word for word in jieba.cut(new_doc)])
        sims = index[model[new_vec]]
        largest = nlargest(sims, 1000) # index
        s = set()
        ten_largest = []
        for n in largest:
            if videotitles[n] not in s:
                s.add(videotitles[n])
                ten_largest.append(videotitles[n])
            if len(ten_largest) == 11:
                break
        if exist:
            ten_largest.pop(0)
        print('十个最相似结果:')
        for w in ten_largest:
            print(w)
