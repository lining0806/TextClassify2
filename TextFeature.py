#coding: utf-8
from __future__ import division
__author__ = 'LiNing'


def TextBool(words_feature, text):
    bool_features = []
    words = sorted(list(set(text)))
    for word_feature in words_feature: # 根据words_feature生成每个text的feature
        if word_feature in words:
            bool_features.append(1)
        else:
            bool_features.append(0)
    return bool_features


def ComputeTf(words_feature, text): # 每个text的tf
    tf_features = []
    for word_feature in words_feature:
        word_count = text.count(word_feature)
        length = len(text)
        tf = word_count/length
        tf_features.append(tf)
    return tf_features
