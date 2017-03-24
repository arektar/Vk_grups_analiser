# -*- coding: utf-8-*-
from gensim.models.word2vec import Word2Vec
import gensim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import os


class Tree_analyser():
    def __init__(self):
        global model
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
                print ("key error: " + word)
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

    def take_groups_vecs(self, groups_base):
        vecs_base={}
        for group in groups_base:
            posts_vects = []
            for post in groups_base[group]:
                sentance_vects = []
                for setence in post:
                    word_vects, words = self.getWordVecs(setence)
                    if len(word_vects) < 1: continue
                    sentance_vects.append(
                        self.middleVect(word_vects))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                posts_vects.append(
                    self.middleVect(sentance_vects))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            vecs_base[group] = self.middleVect(posts_vects)
        return vecs_base



def library_prepearing():
    global model
    print("Загрузка начинается")
    model = gensim.models.KeyedVectors.load_word2vec_format(r'ru_dicts\ruscorpora_mean_hs.model.bin', binary=True)
    print("Загрузка завершена")
    return model


if __name__ == "__main__":
    pass