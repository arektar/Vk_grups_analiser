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

    def take_group_vec(self, group_base):
        posts_vects = []
        for post in group_base:
            if post:
                post_vec = self.take_words_vec(post)
                if post_vec != []:
                    posts_vects.append(post_vec)  # !!!!!!!!!!!!!
        if posts_vects != []:
            group_vec = self.middleVect(posts_vects)
            return group_vec
        else:
            return -1

    def take_words_vec(self, text):
        sentance_vects = []
        for setence in text:
            word_vects, words = self.getWordVecs(setence)
            if len(word_vects) < 1: continue
            sentance_vects.append(
                self.middleVect(word_vects))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if sentance_vects:
            return self.middleVect(sentance_vects)
        else:
            return []


def library_prepearing(button1, button2, path):
    global model
    print("Загрузка начинается")
    model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
    print("Загрузка завершена")
    button1.setEnabled(True)
    button2.setEnabled(True)
    return model


def find_nearest(number, groups_vecdict, text_vec):  # !!!
    simularity_dict = {}
    for group in groups_vecdict:
        similarity = cosine_similarity(groups_vecdict[group], text_vec)
        simularity_dict[group] = abs(similarity)
    second = lambda x: x[1]
    nearest_list = sorted(simularity_dict.items(), key=second, reverse=True)
    nearest_list = nearest_list[:number]
    return nearest_list


if __name__ == "__main__":
    pass
