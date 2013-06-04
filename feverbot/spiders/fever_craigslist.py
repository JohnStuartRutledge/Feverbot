# -*- coding: UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import re
import urlparse
from feverbot.items import CraigsListItem
from scrapy.log import log

class CraigSpider(CrawlSpider):
    """ Spider for crawling Craigslist Austin 
    """
    name            = "CraigslistSpider"
    allowed_domains = ["austin.craigslist.com", "images.craigslist.com"]
    start_urls      = ["http://austin.craigslist.com/"]
    rules = (
            Rule(SgmlLinkExtractor(allow=("/", )), callback='parse_data'),
        )
    
    categories = re.compile(r'^http(.*)\/[A-Za-z]{3}/[A-Za-z]+')
    htmlpages  = re.compile(r'^http(.*)html$')
    searchpage = re.compile(r'^http(.*)\/search\/(.*)')
    
    
    def parse_data(self, response):
        hxs    = HtmlXPathSelector(response)
        items  = []
        images = hxs.select('//img/@src').extract()
        
        for img in images:
            if re.match(r'(.*)craigslist(.*)\.jpg', img):
                item = CraigsListItem()
                item['img_urls'] = []
                
                if re.match(r'^http+', img):
                    imgurl = img
                else:
                    imgurl = urlparse(response.url, img)
                
                item['image_urls'].append(imgurl)
                yield item
            
        for url in hxs.select('//a/@href').extract():
            if self.categories.match(url) \
            or self.htmlpages.match(url) \
            or self.searchpage.match(url):
                yield Request(url, callback=self.parse_data)


