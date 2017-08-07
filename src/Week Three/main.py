import gensim
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from text_representation.tfidf import tfidf_process


if __name__ == '__main__':
    tfidf_process()