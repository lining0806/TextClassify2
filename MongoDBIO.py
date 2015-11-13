#coding: utf-8
from __future__ import division
__author__ = 'LiNing'

import os
import pymongo
import datetime


class MongoDBIO(object):
    # 申明相关的属性
    def __init__(self, host, port, name, password, database, collection):
        self.host = host
        self.port = port
        self.name = name
        self.password = password
        self.database = database
        self.collection = collection

    # 连接数据库，db和posts为数据库和集合的游标
    def Connection(self):
        ## --------------------------------------------------------------------------------
        # # connection = pymongo.Connection() # 连接本地数据库
        # connection = pymongo.Connection(host=self.host, port=self.port)
        # db = connection[self.database]
        # if len(self.name)>0:
        #     db.authenticate(name=self.name, password=self.password) # 验证用户名密码
        # else:
        #     pass
        ## --------------------------------------------------------------------------------
        # mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
        if len(self.name)>0:
            uri = "mongodb://%s:%s@%s:%d/%s" % (self.name, self.password, self.host, self.port, self.database)
        else:
            uri = "mongodb://%s:%d/%s" % (self.host, self.port, self.database)
        # print uri
        client = pymongo.MongoClient(uri)
        db = client.get_default_database()
        ## --------------------------------------------------------------------------------
        print "Database:", db.name
        print db.collection_names() # 查询所有集合
        posts = db[self.collection]
        print "Collection:", posts.name
        print posts.count()

        return posts


# 查询操作
def TrainDataSelect(host, port, name, password, database, collection):
    posts = MongoDBIO(host, port, name, password, database, collection).Connection()
    print "Number of All Documents in the Collection:", posts.count() # 查询数量

    train_datas_targets = {"datas":[], "targets":[]}
    #-------------------------------------------------------------------------------
    # 以下几行根据实际情况修改
    starttime = datetime.datetime(2015, 1, 1)
    endtime = datetime.datetime.now()
    for post in posts.find({
        "content":{"$exists":1},
        "country":{"$exists":1},
        "createdtime":{"$gte":starttime, "$lte":endtime},
        "t_status":1
    }):
        # print post
        # if len(post["content"])>1 and len(post["country"])>1:
        if (post["content"] and post["country"]) is not None:
            train_datas_targets["datas"].append(post["content"])
            Classify_Dimension = {u"国家":post["country"]} ## 支持多维分类
            train_datas_targets["targets"].append(Classify_Dimension)
        else:
            print '{"_id":ObjectId("%s")}' % post["_id"]
    #-------------------------------------------------------------------------------
    print "Number of Selected Train Documents in the Collection:", len(train_datas_targets["datas"]) # 选择数量
    return train_datas_targets


def TestDataSelect(host, port, name, password, database, collection, Limit_Number):
    posts = MongoDBIO(host, port, name, password, database, collection).Connection()
    print "Number of all Documents in the Collection:", posts.count() # 查询数量

    test_ids_datas = {"ids":[], "datas":[]}
    #-------------------------------------------------------------------------------
    # 以下几行根据实际情况修改
    starttime = datetime.datetime(2015, 1, 1)
    endtime = datetime.datetime.now()
    for post in posts.find({
        "content":{"$exists":1},
        "country":{"$exists":0},
        "createdtime":{"$gte":starttime, "$lte":endtime},
        "t_status":{"$ne":1}
    }).sort("createdtime", pymongo.DESCENDING).limit(Limit_Number):
        # print post
        # if len(post["content"])>1:
        if post["content"] is not None:
            test_ids_datas["ids"].append(post["_id"])
            test_ids_datas["datas"].append(post["content"])
        else:
            print '{"_id":ObjectId("%s")}' % post["_id"]
    #-------------------------------------------------------------------------------
    print "Number of Selected Test Documents in the Collection:", len(test_ids_datas["datas"]) # 选择数量
    return test_ids_datas


# 更新操作
def ResultUpdate(test_host, test_port, test_name, test_password, test_database, test_collection, test_ids_targets):
    posts = MongoDBIO(test_host, test_port, test_name, test_password, test_database, test_collection).Connection()
    test_ids = test_ids_targets["ids"]
    test_targets = test_ids_targets["targets"]

    for i in range(len(test_ids)):
        id = test_ids[i]
        test_target = test_targets[i]
        #-------------------------------------------------------------------------------
        # 以下几行根据实际情况修改
        # posts.update({"_id":id}, {"$set":{"country_test":test_target[u"国家"], "t_status":1}}) ## 支持多维分类
        posts.update({"_id":id}, {"$set":{"country_test":test_target[u"国家"]}}) ## 支持多维分类
        #-------------------------------------------------------------------------------
        print '{"_id":ObjectId("%s")}' % id # MongoVUE中find命令
