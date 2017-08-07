import jieba
from os import mkdir
from os import path

videotitle_path = r'..\..\data\videotitle'

if not path.exists(r'.\temp'):
    mkdir(r'.\temp')


def read_titles() -> list:
    with open(videotitle_path, 'r') as videotitle:
        videotitles = [line.replace('\n', '') for line in videotitle]
    return videotitles


def split_words(videotitles) -> list:
    result = [[word for word in jieba.cut(videotitle)] for videotitle in videotitles]
    return result


def pre_process():
    videotitles = read_titles()
    words = split_words(videotitles)
    sentences = (' '.join(word) for word in words)
    with open(r'./temp/sentences.txt', 'w', encoding='utf-8') as f:
        for line in sentences:
            f.write(line + '\n')


def get_sentences() -> list:
    if not path.isfile(r'./temp/sentences.txt'):
        print('sentences.txt not found, rebuilding...')
        pre_process()
    with open(r'./temp/sentences.txt', 'r', encoding='utf-8') as f:
        result = [line.replace('\n', '') for line in f]
    return result


def count_words():
    s = split_words(read_titles())
    s = set([item for sen in s for item in sen])
    print(len(s))
    # 89721

