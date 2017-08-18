import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from multiprocessing import cpu_count

from .reader import pre_process


def word2vec():
    pre_process()

    infile = r'./temp/sentences.txt'
    outfile = r'./temp/model'
    model = Word2Vec(LineSentence(infile), size=400, window=5, min_count=5, sg=0, workers=cpu_count())
    model.save(outfile)
    model.wv.save_word2vec_format(outfile + '.vector', binary=False)

    model = gensim.models.KeyedVectors.load_word2vec_format(r'./temp/model.vector')
    model.save_word2vec_format(outfile + '.vector')
