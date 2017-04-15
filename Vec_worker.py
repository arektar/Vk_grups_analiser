# -*- coding: utf-8-*-
from gensim.models.word2vec import Word2Vec
import gensim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
import os
import scipy


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
                print("key error: " + word)
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
        vecs_base = {}
        for group in groups_base:
            posts_vects = []
            for post in groups_base[group]:
                posts_vects.append(self.take_words_vec(post))  # !!!!!!!!!!!!!
            vecs_base[group] = self.middleVect(posts_vects)
        return vecs_base

    def take_words_vec(self, text):
        sentance_vects = []
        for setence in text:
            word_vects, words = self.getWordVecs(setence)
            if len(word_vects) < 1: continue
            sentance_vects.append(
                self.middleVect(word_vects))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self.middleVect(sentance_vects)

    def start(self, work_wind):
        pass


def library_prepearing():
    global model
    print("Загрузка начинается")
    model = gensim.models.KeyedVectors.load_word2vec_format(r'ru_dicts\ruscorpora_mean_hs.model.bin', binary=True)
    print("Загрузка завершена")
    return model


def find_nearest(number, groups_vecdict, text_vec):  # !!!
    simularity_dict = {}
    for vec in groups_vecdict:
        similarity = cosine_similarity(vec[1], text_vec)
        simularity_dict[vec] = similarity
    second = lambda x: x[1]
    nearest_list = sorted(simularity_dict.items(), key=second, reverse=True)
    return nearest_list[:number]


if __name__ == "__main__":
    pass
