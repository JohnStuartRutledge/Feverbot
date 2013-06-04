# -*- coding: UTF-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider
# from feverbot import settings

#-----------------------------------------------------------------------------
# ACTIVATE DJANGO ENVIRONMENT
#-----------------------------------------------------------------------------

import sys, os, imp
from django.core.management import setup_environ

# get root directory of Django project
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))

# check if path to Django project is in
# the system path; if not, then add it
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# set your PYTHONPATH variable incase your working in a virtual environment
os.environ['PYTHONPATH'] = ROOT

# create an environment variable for locating your django settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# locate, and load your django settings file
f, filename, desc = imp.find_module('settings', [ROOT])
settings = imp.load_module('settings', f, filename, desc)

# setup the django environment
setup_environ(settings)

# import your Django models
from myproject.apps.biz.models import Business, Website

# from django.utils.dateformat import DateFormat

# these are the Django id's for each website in the fever_website_types table
website_ids = {
    'HomeSpider':         1,
    'BlogSpider':         2,
    'FacebookSpider':     3,
    'TwitterSpider':      4,
    'YelpSpider':         5,
    'YoutubeSpider':      6,
    'AptratingsSpider':   7,
    'GoogleplacesSpider': 8,
    'CraigslistSpider':   9
}

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------

class FeverBaseSpider(CrawlSpider):
    
    props = None
    
    def __init__(self, *a, **kw):
        '''The base spider for Insight Fever from which all other
        spiders will inherit. Its most notable feature are querys
        to the Django database to get sites for scraping
        '''
        super(FeverBaseSpider, self).__init__(*a, **kw)
        
        # create buffer to store items you dont want exported immediately
        self.items_buffer = {}
        
        if not hasattr(self, 'props'):
            self.props = self._get_biz_urls()
        
        # get a list of all our clients and their associated id's
        # {1: 'Mindwink', 2: 'Villages'}
        self.BIZ = {x['id']:x['biz_name'] for x in \
                        Business.objects.values('id', 'biz_name')}
    
    def _get_biz_urls(self):
        '''Takes the name of the site your scraping (Yelp, Facebook) 
        and returns a dictionary of URLs to scrape along with their 
        matching biz id (key=url, val=biz.id)
        '''
        # use the name of the scraper to get the right website id
        site_id = website_ids[self.name]
        if not site_id:
            raise CloseSpider('your spiders name has no matching id')
        
        # create list of all websites to scrape for the given site id
        site_list = Website.objects.values(
                    'business', 'site_url').filter(site_type=site_id)
        
        if site_list:
            props = { x['site_url']: x['business'] \
                      for x in site_list if x['site_url'] }
        else:
            raise CloseSpider('No Matching Businesses\
             found in Django Database')
        return props

