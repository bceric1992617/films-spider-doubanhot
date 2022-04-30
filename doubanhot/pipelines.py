# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql 
import scrapy
import os
import shutil
import time
import datetime
from scrapy.pipelines.images import ImagesPipeline
from doubanhot.settings import IMAGES_STORE
from doubanhot.getFilmMsg import getFilmMsg


class doubanhotPipeline: 
    def __init__(self):
        self.db = pymysql.connect(
            host="localhost",
            port=3306, 
            db='films', 
            user='root', 
            passwd='123321', 
            charset='utf8'
        )
        self.db_cur = self.db.cursor()

    def process_item(self, item, spider):
        #更新和插入信息
        self.updateMsg(item)
        self.db.commit() 
        return item

    def updateMsg(self, item):
        for v in item['data']:
            insertSql = 'insert into hot(filmsId,filmsName,videoType,createTime,updateTime,isDel) values(%s,%s,%s,%s,%s,%s)'
            updateSql ='update films set douban=%s where filmsId=%s'
            title = v['title'].replace(' ','')
            self.db_cur.execute("select filmsId from films where filmsName= '"+ title +"' limit 1;")
            filmMsg = self.db_cur.fetchone()
            if bool(filmMsg) :
                self.db_cur.execute(updateSql, [
                    v['rate'],
                    filmMsg
                ])

                self.db_cur.execute(insertSql, [
                    filmMsg,
                    title,
                    item['type'],
                    int(round(time.time())),
                    int(round(time.time())),
                    0            
                ])
            
            




        

