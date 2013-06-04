# encoding=utf-8

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonLinesItemExporter
from scrapy.contrib.exporter import JsonItemExporter
from scrapy import log
from feverbot.fever_utils import make_filename, FeverException, get_biz_urls
from scrapy.exceptions import DropItem
from scrapy.stats import stats
from feverbot.items import Apt, AptReview

from exporters import FeverJsonItemExporter
import json
import os


class FeverbotPipeline(object):
    '''Pipeline for writing scrapped items to a Json file
    '''
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        '''Initialize your exporters when spider first starts
        '''
        log.msg('\n\n{0}\n{1}\n{2}\n\n'.format('-'*79, spider.name, '-'*79), log.INFO)

        # figure out which fields to export based on the spiders name
        # this also exports the fields in the specified order
        if spider.name == 'YelpSpider':
            foo_fields = [
                    'biz_id',
                    'timestamp',
                    'stars',
                    'review_count'
                ]
        elif spider.name == 'AptratingsSpider':
            foo_fields = [
                    'biz_id',
                    'recommended_by',
                    'total_overall_rating',
                    'overall_parking',
                    'overall_maintenance',
                    'overall_construction',
                    'overall_noise',
                    'overall_grounds',
                    'overall_safety',
                    'overall_office_staff',

                    'comment_url',
                    'comment_title',
                    'comment_username',
                    'comment_post_date',
                    'comment_years_stayed',
                    'comment_message',
                    'last_edited',
                    'replies',

                    'overall_rating',
                    'parking',
                    'maintenance',
                    'construction',
                    'noise',
                    'grounds',
                    'safety',
                    'office_staff'
                ]
        else:
            raise FeverException('a foo_fields variable is not yet \
            defined for "{0}"'.format(spider.name))

        # create a unique filename
        self.file = open(os.path.join('data',
                            make_filename(spider.name, 'json')), 'w+b')

        self.json_exporter = FeverJsonItemExporter(
                                self.file,
                                fields_to_export=foo_fields,
                                sort_keys=True,
                                indent=2)

        # start exporting items to JSON file
        self.json_exporter.start_exporting()


    def process_item(self, item, spider):
        '''Process scraped items one at a time
        '''
        # create nested dict here?
        self.json_exporter.export_item(item)
        return item


    def spider_closed(self, spider):
        '''Close your exporters now that the spider is done scraping'''
        self.json_exporter.finish_exporting()



class TestPipeline(object):
    '''For test development only
    '''
    def __init__(self):
        self.d = {} # change to OrderedDict


    def spider_opened(self, spider):
        '''Initialize your exporters when spider first starts
        '''
        if spider.name == 'AptratingsSpider':
            BIZ_DICT, PROPS = get_biz_urls("Apartment Ratings")

        for k, v in PROPS.items():
            self.d[v] = {
              "url"    : k,
              # "stats"  : stats.get_stats(), # this goes at end
              "totals" : {
                  "overall_construction": -1,
                  "overall_grounds"     : -1,
                  "overall_maintenance" : -1,
                  "overall_noise"       : -1,
                  "overall_office_staff": -1,
                  "overall_parking"     : -1,
                  "overall_safety"      : -1,
                  "recommended_by"      : -1,
                  "total_overall_rating": -1
              },
              "comments" : []
            }


    def process_item(self, item, spider):
        '''Process scraped items one at a time
        '''
        # val_dict = item.__dict__['_values']
        # val_dict['link_url']
        if item['name'] in self.foo_dict:
            raise DropItem('Duplicate found %s' % item)
        else:
            pass

        if isinstance(item, Apt):
            # process item
            pass

        return item

    def spider_closed(self, spider):
        '''Close your exporters now that the spider is done scraping
        '''
        # http://doc.scrapy.org/en/latest/topics/stats.html
        # stats.get_stats()
        self.json_exporter.finish_exporting()

