from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy import log
#from scrapy.contrib.spiders import Rule
from feverbot.items import Yelp
from feverbot.fever_utils import now, get_biz_urls

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------

BIZ_DICT, PROPS = get_biz_urls("Yelp")

class YelpSpider(BaseSpider):
    '''Spider for crawling Yelp and extracting ratings data
    To use, first cd into your Scrapy project directory. then:
    >>> scrapy crawl YelpSpider
    '''
    name            = 'YelpSpider'
    allowed_domains = ['http://www.yelp.com']
    start_urls      = PROPS.keys()

    def parse(self, response):
        '''Parse the data out of Yelps HTML page
        '''
        hxs = HtmlXPathSelector(response)
        ylp = Yelp()
        url = response.url

        if response.status == 302:
            self.log('302: Redirected', level=log.INFO)

        # get the time at which this scrape is occuring
        ylp['timestamp'] = now

        # If there are stars to be found, grab them.
        stars = hxs.select('string(//div[@id="biz-vcard"]//img[contains(@alt, "rating")]/@alt)').extract()
        try:
            ylp['stars'] = float(stars[0].split(' ')[0])
        except ValueError:
            self.log('No stars were found at the URL: {0}'.format(url), level=log.INFO)
            ylp['stars'] = 0

        # get the count for the number of reviews customers have left on the Yelp profile
        review_count = hxs.select('//span[@class="count"]/text()').extract()
        ylp['review_count'] = int(review_count[0]) if review_count else 0

        # get the biz_id from the current URL
        try:
            ylp['biz_id'] = PROPS[url]
        except KeyError:
            # try and see if a partial match took place AKA if we were redirected
            ylp['biz_id'] = [PROPS[site] for site in PROPS.keys() if site in url]
            ylp['biz_id'] = ylp['biz_id'][0] if ylp['biz_id'] else 0

        return ylp


