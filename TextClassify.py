#coding: utf-8
from __future__ import division
__author__ = 'LiNing'
import datetime


def Gne_Train_Dimensions(train_targets):
    dimensions = train_targets[0].keys()
    train_targets_names_dimensions = [] # 每个维度下的分类名称
    train_targets_dimensions = [] # 每个维度下的分类情况
    for dimension in dimensions:
        temp = [train_target[dimension] for train_target in train_targets]
        temp_list = sorted(list(set(temp)))
        # 统计每个分类名称下的数目
        print 'The Classify Dimension "', dimension, '":'
        for train_targets_names in temp_list:
            print train_targets_names, "\t", temp.count(train_targets_names)
        temp_num = [temp_list.index(temp_i) for temp_i in temp]
        train_targets_names_dimensions.append(temp_list)
        train_targets_dimensions.append(temp_num)
    return train_targets_names_dimensions, train_targets_dimensions


def TextClassifier(fea_train, fea_test, train_targets_dimensions):
    results = []

    ######################################################
    # # Multinomial Naive Bayes Classifier
    # from sklearn.naive_bayes import MultinomialNB
    # nbcclf = MultinomialNB() # default with alpha = 1.0 # 分类器模型
    # nbcclf.fit(fea_train, train_targets_dimensions) # 分类器训练
    # pred = nbcclf.predict(fea_test) # 分类器识别
    # # print "*************************\nMultinomial Naive Bayes Classifier (Gaussian likelihood)\n*************************"
    # results.append(list(pred))
    ######################################################
    # Linear SVM Classifier (Linear kernel)
    from sklearn.svm import LinearSVC
    lsvclf = LinearSVC()
    lsvclf.fit(fea_train, train_targets_dimensions)
    pred = lsvclf.predict(fea_test)
    # print "*************************\nLinear SVM Classifier (Linear kernel)\n*************************"
    results.append(list(pred))
    ######################################################
    # # Decision Tree
    # from sklearn.tree import DecisionTreeClassifier
    # dtclf = DecisionTreeClassifier() # default with criterion = "gini"
    # dtclf.fit(fea_train, train_targets_dimensions)
    # pred = dtclf.predict(fea_test)
    # # print "*************************\nDecision Tree\n*************************"
    # results.append(list(pred))
    ######################################################
    # # Ensemble (Random Forests)
    # from sklearn.ensemble import RandomForestClassifier
    # rfclf = RandomForestClassifier() # default with n_estimators = 10
    # rfclf.fit(fea_train, train_targets_dimensions)
    # pred = rfclf.predict(fea_test)
    # # print "*************************\nEnsemble (Random Forests)\n*************************"
    # results.append(list(pred))
    ######################################################
    # # Neighbors
    # from sklearn.neighbors import KNeighborsClassifier
    # knnclf = KNeighborsClassifier() # default with n_neighbors = 5
    # knnclf.fit(fea_train, train_targets_dimensions)
    # pred = knnclf.predict(fea_test)
    # # print "*************************\nNeighbors\n*************************"
    # results.append(list(pred))
    ######################################################

    # ######################################################
    # # SVM Classifier
    # from sklearn.svm import SVC
    # from sklearn.svm import LinearSVC
    # from sklearn import preprocessing
    # from sklearn.decomposition import PCA
    # from sklearn.pipeline import Pipeline
    # from sklearn.grid_search import GridSearchCV
    # from sklearn.cross_validation import StratifiedKFold
    # from sklearn.cross_validation import KFold
    # fea_train = preprocessing.MinMaxScaler().fit_transform(fea_train)
    # parameters = {
    #     'pca__n_components':[50, 100, 150, 200, 250, 300],
    #     'svm__kernel':['rbf', 'linear'],
    #     'svm__gamma':[1e-2, 1e-1],
    #     'svm__C':[1e-2, 1e-1, 1, 5, 10]
    # }
    # pipeline = Pipeline(
    #     steps = [
    #         ('pca', PCA()),
    #         ('svm', SVC())
    #     ]
    # )
    # clf = GridSearchCV(
    #     estimator = pipeline,
    #     param_grid = parameters,
    #     cv = StratifiedKFold(train_targets_dimensions, 3),
    #     scoring = "accuracy",
    #     n_jobs = 3
    # )
    # clf.fit(fea_train, train_targets_dimensions)
    # pred = clf.predict(fea_test)
    # # print "*************************\n SVM Classifier \n*************************"
    # results.append(list(pred))
    # ######################################################

    return results


def Vote(votelist):
    elements_dict = {}
    for element in votelist:
        if elements_dict.has_key(element):
            elements_dict[element] += 1
        else:
            elements_dict[element] = 1
    # key函数利用词频进行降序排序
    elements_sortlist = sorted(elements_dict.items(), key=lambda f:f[1], reverse=True) # 内建函数sorted参数需为list
    return elements_sortlist[0][0]
