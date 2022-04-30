# -*- coding: utf-8 -*-
import scrapy
import json
import os
import time
import datetime
import sys
import re
import pymysql
from urllib.parse import quote
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from doubanhot.items import doubanhotItem
from scrapy import Spider, Request



class doubanhot(CrawlSpider):
    name = 'doubanhot'
    allowed_domains = [
        'douban.com'
    ]

    urlList = [
        'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=最新&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=欧美&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=华语&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=韩国&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=日本&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=经典&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=豆瓣高分&sort=recommend&page_limit=20&page_start=0',
        
        'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=最新&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=欧美&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=华语&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=韩国&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=日本&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=经典&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=movie&tag=豆瓣高分&sort=recommend&page_limit=20&page_start=20',

        'https://movie.douban.com/j/search_subjects?type=tv&tag=热门&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=美剧&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=英剧&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=韩剧&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=日剧&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=国产剧&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=港剧&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=日本动画&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=纪录&sort=recommend&page_limit=20&page_start=0',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=综艺&sort=recommend&page_limit=20&page_start=0',

        'https://movie.douban.com/j/search_subjects?type=tv&tag=热门&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=美剧&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=英剧&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=韩剧&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=日剧&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=国产剧&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=港剧&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=日本动画&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=纪录&sort=recommend&page_limit=20&page_start=20',
        'https://movie.douban.com/j/search_subjects?type=tv&tag=综艺&sort=recommend&page_limit=20&page_start20',
    ]
    
    def start_requests(self):
        for v in self.urlList:
            yield Request(v, self.parseHotMsg)
    
    def parseHotMsg(self, response):    
        item = doubanhotItem()
        item['data'] = json.loads(response.body)['subjects']
        item['type'] = 0 
        url = response.url.split('?')[1]
  
        if url.find('movie') > -1 :
            if url.find(quote('热门')) > -1 :
                item['type'] = 1
            elif url.find(quote('最新')) > -1 :
                item['type'] = 2
            elif url.find(quote('欧美')) > -1 :
                item['type'] = 3
            elif url.find(quote('华语')) > -1 :
                item['type'] = 4
            elif url.find(quote('韩国')) > -1 :
                item['type'] = 5
            elif url.find(quote('日本')) > -1 :
                item['type'] = 6
            elif url.find(quote('经典')) > -1 :
                item['type'] = 7
            elif url.find(quote('豆瓣高分')) > -1 :
                item['type'] = 8

        elif url.find('tv') > -1 :
            if url.find(quote('热门')) > -1 :
                item['type'] = 100
            elif url.find(quote('美剧')) > -1 :
                item['type'] = 101
            elif url.find(quote('英剧')) > -1 :
                item['type'] = 102
            elif url.find(quote('韩剧')) > -1 :
                item['type'] = 103
            elif url.find(quote('日剧')) > -1 :
                item['type'] = 104
            elif url.find(quote('国产')) > -1 :
                item['type'] = 105
            elif url.find(quote('港剧')) > -1 :
                item['type'] = 106
            elif url.find(quote('日本动画')) > -1 :
                item['type'] = 107
            elif url.find(quote('纪录')) > -1 :
                item['type'] = 108
            elif url.find(quote('综艺')) > -1 :
                item['type'] = 109

        return item





      