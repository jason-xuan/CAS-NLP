# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from os import path
import jieba


shakespeare_path = '..\\..\\data\\shakespeare-merchant.trec'


def _get_docs() -> list:

    with open(path.join(shakespeare_path, 'shakespeare-merchant.trec.1')) as f:
        xml1 = f.read()

    with open(path.join(shakespeare_path, 'shakespeare-merchant.trec.2')) as f:
        xml2 = f.read()

    soup1 = BeautifulSoup(xml1, "lxml")
    soup2 = BeautifulSoup(xml2, "lxml")

    docs = soup1.find_all('doc') + soup2.find_all('doc')

    return docs


def _find_ban(docs: list) -> list:
    """
    为了去除掉标点符号
    获取标点符号的列表
    """
    full_text = "".join(["".join([string for string in doc.strings]) for doc in docs])
    l = [x for x in jieba.cut(full_text) if len(x) == 1]
    l = set(l)
    num = set([str(n) for n in range(0, 10)])
    lower = set([chr(x) for x in range(ord('a'), ord('z') + 1)])
    upper = set([chr(x) for x in range(ord('A'), ord('Z') + 1)])
    ban = l - num - lower - upper

    return list(ban)


class Doc(object):
    """
    Easily represent document in the data set.
    """
    docs = _get_docs()
    ban_list = _find_ban(docs)
    _processed_list = None
    _processed_dict = None
    _inverse_dit = None

    def __init__(self, doc):
        # 固有属性
        self.docno = doc.docno.text
        self.title = doc.title.text

        self.strings = [string for string in doc.strings]
        self.full_text = "".join(self.strings).replace('\n', ' ').replace('\t', ' ')

        # process
        self.word_list = [x for x in jieba.cut(self.full_text) if x not in Doc.ban_list]
        self.word_set = set(self.word_list)

    def __str__(self) -> str:
        title = self.title.replace('\n', ' ').replace('\t', ' ')
        return '<docno :\t{0}, \ttitle :\t{1}>'.format(self.docno, title)

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def get_processed(cls) -> list:

        if cls._processed_list is None:
            cls._processed_list = [Doc(doc) for doc in cls.docs if doc.docno.text != 'SHK-MOV-interval']
        return cls._processed_list

    @classmethod
    def get_dict(cls) -> dict:

        if cls._processed_dict is None:
            processed = cls.get_processed()
            cls._processed_dict = {doc.docno : doc for doc in processed}
        return cls._processed_dict

    @classmethod
    def get_inverse_dit(cls) -> dict:
        if cls._inverse_dit is None:
            processed = cls.get_processed()
            cls._inverse_dit = {}
            for doc in processed:
                for word in doc.word_set:
                    if word not in cls._inverse_dit:
                        cls._inverse_dit[word] = [doc.docno]
                    else:
                        cls._inverse_dit[word].append(doc.docno)
        return cls._inverse_dit

