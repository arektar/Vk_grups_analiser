# -*- coding: utf-8-*-
from gensim.models.word2vec import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import os


class Tree_analyser():
    def __init__(self, for_analyse):
        global model
        self.tree = for_analyse
        self.model = model
        self.ts = TSNE(2)

    def getWordVecs(self, words_list):
        vecs = []
        good_words = []
        # words_list = []
        print(words_list)
        for word in words_list:
            # word = word.replace('\n', '')
            # print (word)
            try:
                vecs.append(self.model[word].reshape((1, 300)))
                good_words.append(word)
            except KeyError:
                print (b"key error: " + word)
                # print (self.model[word].reshape((1,300)))

        if vecs: vecs = np.concatenate(vecs)
        return np.array(vecs, dtype='float'), good_words  # TSNE expects float type values

    def middleVect(self, veclists):
        middle_veclist = []
        i = 0
        while i < len(veclists[0]):
            summ = float(0)
            for list_vecs in veclists: summ += list_vecs[i]
            middle_veclist.append(summ / len(veclists))
            i += 1
        return np.array(middle_veclist, dtype='float')

    def take_vect(self):
        posts_vects = []
        for post in self.tree:
            sentance_vects = []
            for setence in post:
                word_vects, words = self.getWordVecs(setence)
                if len(word_vects) < 1: continue
                sentance_vects.append(
                    self.middleVect(word_vects))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            posts_vects.append(
                self.middleVect(sentance_vects))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self.middleVect(posts_vects)


def library_prepearing():
    global model
    print("Загрузка начинается")
    model = Word2Vec.load_word2vec_format(r'ru_dicts\ruscorpora_mean_hs.model.bin', binary=True)
    print("Загрузка завершена")
    return model
