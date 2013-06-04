# encoding=utf-8

from scrapy.contrib.exporter import CsvItemExporter
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.contrib.exporter import JsonLinesItemExporter
#from scrapy.contrib.exporter import XmlItemExporter
from scrapy.contrib.exporter import BaseItemExporter

import json

class FeverJsonItemExporter(JsonItemExporter):
    '''Pipeline for regular Json Files that overwrites Scrapys
    JsonItemExporter to allow the dont_fail=True argument
    as well as the ability to pass in JSONEncoder arguments.
    '''
    def __init__(self, json_file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file       = json_file
        self.encoder    = json.JSONEncoder(**kwargs)
        self.first_item = True
