# coding: utf-8
from __future__ import division
__author__ = 'LiNing'

import re
from os.path import exists
import simplejson as json

from MongoDBIO import TrainDataSelect
from MongoDBIO import TestDataSelect
from MongoDBIO import ResultUpdate

from TextProcess import TextSeg
from TextProcess import TextExtractTags
from TextProcess import MakeAllWordsList
from TextProcess import MakeFeatureWordsDict
from TextProcess import MakeStopWordsList

from TextFeature import TextBool
from TextFeature import ComputeTf

from TextClassify import Gne_Train_Dimensions
from TextClassify import TextClassifier
from TextClassify import Vote

import numpy as np


if __name__ == '__main__':
#-------------------------------------------------------------------------------
    try:
        with open("./Config/config", "r") as fp:
            lines = fp.readlines() # list
    except Exception as e:
        print e
        exit()
    for line in lines:
        # 检测语言
        if re.match(r'^lag', line):
            lag = str(re.search(r'"(.*?)"', line).group(1)) # 从任意位置只找出第一个成功的匹配
        # 特征词典维度
        elif re.match(r'^dict_size', line):
            dict_size = int(re.search(r'.*?\s*=\s*(\d+?)\s', line).group(1))
        # 训练集配置
        elif re.match(r'^train_host', line):
            train_host = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^train_port', line):
            train_port = int(re.search(r'.*?\s*=\s*(\d+?)\s', line).group(1))
        elif re.match(r'^train_name', line):
            train_name = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^train_password', line):
            train_password = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^train_database', line):
            train_database = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^train_collection', line):
            train_collection = str(re.search(r'"(.*?)"', line).group(1))
        # 测试集配置
        elif re.match(r'^test_host', line):
            test_host = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^test_port', line):
            test_port = int(re.search(r'.*?\s*=\s*(\d+?)\s', line).group(1))
        elif re.match(r'^test_name', line):
            test_name = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^test_password', line):
            test_password = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^test_database', line):
            test_database = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^test_collection', line):
            test_collection = str(re.search(r'"(.*?)"', line).group(1))
        elif re.match(r'^limit_number', line):
            limit_number = int(re.search(r'.*?\s*=\s*(\d+?)\s', line).group(1))


#-------------------------------------------------------------------------------
    # 训练集数据提取与分词
    json_path = "./Config/traindata_"+lag # 训练数据库变化需删除重新生成
    if not exists(json_path):
        try:
            train_datas_targets = TrainDataSelect(train_host, train_port, train_name, train_password, train_database, train_collection)
        except Exception as e:
            print e
            exit()
        train_datasseg = TextSeg(train_datas_targets["datas"], lag)
        # 由训练集生成单词库all_words_list
        all_words_list = MakeAllWordsList(train_datasseg)
        train_datasseg_targets_wordlist = {"datas":train_datasseg, "targets":train_datas_targets["targets"], "wordlist":all_words_list}
        with open(json_path, 'wb') as train_file:
            json.dump(train_datasseg_targets_wordlist, train_file)
    else:
        with open(json_path, 'rb') as json_file:
            train_datasseg_targets_wordlist = json.load(json_file)

    train_datasseg = train_datasseg_targets_wordlist["datas"] # list list
    train_targets = train_datasseg_targets_wordlist["targets"] # dict list
    all_words_list = train_datasseg_targets_wordlist["wordlist"] # list


#-------------------------------------------------------------------------------
    # 由训练集生成特征词word_features
    stopwords_file = "./Config/stopwords_"+lag
    stopwords_list = MakeStopWordsList(stopwords_file)
    words_feature = MakeFeatureWordsDict(all_words_list, stopwords_list, dict_size, lag)

    train_targets_names_dimensions, train_targets_dimensions = Gne_Train_Dimensions(train_targets)

    # 训练集特征提取和关键词提取
    fea_train = []
    keywords_train = []
    for train_dataseg in train_datasseg:
        # 特征提取
        train_bool_features = TextBool(words_feature, train_dataseg)
        fea_train.append(train_bool_features)
        # train_tf_features = ComputeTf(words_feature, train_dataseg)
        # fea_train.append(train_tf_features)

        # 关键词提取(利用词频tf)
        train_tags = TextExtractTags(words_feature, train_dataseg, 3)
        # print "The KeyWords:",
        # for i in range(len(train_tags)):
        #     print train_tags[i],
        # print ""
        keywords_train.append(train_tags)
    fea_train = np.array(fea_train)


#-------------------------------------------------------------------------------
    # 测试集数据提取与分词
    try:
        test_ids_datas = TestDataSelect(test_host, test_port, test_name, test_password, test_database, test_collection, limit_number)
    except Exception as e:
        print e
        exit()
    test_datasseg = TextSeg(test_ids_datas["datas"], lag)
    test_ids_datasseg = {"ids":test_ids_datas["ids"], "datas":test_datasseg}

    test_ids = test_ids_datasseg["ids"]
    test_datasseg = test_ids_datasseg["datas"]


#-------------------------------------------------------------------------------
    # 测试集特征提取和关键词提取
    fea_test = []
    keywords_test = []
    for test_dataseg in test_datasseg:
        # 特征提取
        test_bool_features = TextBool(words_feature, test_dataseg)
        fea_test.append(test_bool_features)
        # test_tf_features = ComputeTf(words_feature, test_dataseg)
        # fea_test.append(test_tf_features)

        # 关键词提取
        test_tags = TextExtractTags(words_feature, test_dataseg, 3)
        # print "The KeyWords:",
        # for i in range(len(test_tags)):
        #     print test_tags[i],
        # print ""
        keywords_test.append(test_tags)
    fea_test = np.array(fea_test)


#-------------------------------------------------------------------------------
    # 分类器
    dimensions = train_targets[0].keys()
    all_pred_results = []
    for i in range(len(dimensions)):
        train_targets_dimension = np.array(train_targets_dimensions[i])
        results = TextClassifier(fea_train, fea_test, train_targets_dimension)
        results = np.array(results)
        resultsT = results.T
        # 投票法
        print 'Combination of All the Classifiers for Classify Dimension "', dimensions[i], '":'
        print "The Result of Combination:",
        pred_results = []
        for resultT in resultsT:
            temp_num = Vote(list(resultT))
            pred_result = train_targets_names_dimensions[i][temp_num]
            pred_results.append(pred_result)
            print pred_result,
        print ""
        all_pred_results.append(pred_results)

    # 处理多维度分类结果
    all_pred_results = np.array(all_pred_results)
    all_pred_resultsT = all_pred_results.T
    test_targets = []
    for all_pred_resultT in all_pred_resultsT:
        test_target = {}
        for i in range(len(dimensions)):
            test_target[dimensions[i]] = list(all_pred_resultT)[i]
        test_targets.append(test_target)
    test_ids_targets = {"ids":test_ids, "targets":test_targets}

#-------------------------------------------------------------------------------
    # 更新操作
    if test_host:
        ResultUpdate(test_host, test_port, test_name, test_password, test_database, test_collection, test_ids_targets)
    else:
        print "error"
        exit()
