# -*- coding: utf-8 -*-import os

import sqlite3 as sqlite
# import json
from scrapy import log
from scrapy import signals
from scrapy.stats import stats
from scrapy.exceptions import DropItem
from scrapy.xlib.pydispatch import dispatcher
# from scrapy.contrib.exporter import JsonLinesItemExporter
# from feverbot.fever_utils import make_filename, FeverException, get_biz_urls
# from feverbot.items import Apt, AptReview
# from exporters import FeverJsonItemExporter

class SqlitePipeline(object):
    def __init__(self):
        ''' Pipeline for storing scraped items into sqlite DB
        '''
        try:
            self.con = sqlite.connect('./feverbot.db3',
                                       detect_types=sqlite.PARSE_DECLTYPES)
            self.cur = self.con.cursor()
        except sqlite.OperationalError:
            exit(1)
        
        # import sql schemas
        with open('./feverbot.sql', 'r') as f:
            schema = f.read()
        self.cur.executescript(schema)
        
        # start the party
        # dispatcher.connect(self.spider_opened, signals.spider_opened)
        # dispatcher.connect(self.spider_closed, signals.spider_closed)
    
    def __del__(self):
        self.con.close()
    
    def dbcommit(self):
        self.con.commit()
    
    def handle_error(self, e):
        log.err(e)
    
    def process_item(self, spider, item):
        '''Process the scrapped items for output to sqlite
        '''
        # log.msg("Item stored : " % item, level=log.DEBUG)
        return item
    
    def spider_opened(self, spider):
        '''Initialize your exporters when spider first starts
        '''
        if spider.name == 'AptratingsSpider':
            BIZ_DICT, PROPS = get_biz_urls("Apartment Ratings")
        elif spider.name == 'YelpSpider':
            BIZ_DICT, PROPS = get_biz_urls("Yelp")
        elif spider.name == 'CraigslistSpider':
            BIZ_DICT, PROPS = get_biz_urls("Craigs List")
        else:
            pass
            
    
    def spider_closed(self, spider):
        '''Close your exporters now that the spider is done scraping
        '''
        # stats.get_stats()
        # self.json_exporter.finish_exporting()
        pass




"""
self.cur.execute("SELECT * FROM apt where url=%s" % item['url'])
if self.cur.fetchone():
    log.msg("Item already in database: {0}".format(item), level=log.DEBUG)
    raise DropItem('Duplicate found %s' % item)
else:
    self.cur.execute(
        "INSERT INTO apt (url) VALUES (?)",
        (item['url'][0], item['desc'][0])
    )
    self.con.commit()
"""


