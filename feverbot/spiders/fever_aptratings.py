# -*- coding: UTF-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy.selector import HtmlXPathSelector
from urlparse import urljoin
from scrapy import log
from feverbot.items import Apt, AptReview
from feverbot.fever_utils import now, get_biz_urls, autoViv, replace_txt
from feverbot.fever_utils import replace_escape_chars as esc_chars

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------

# return a list of all apartment-ratings URL's you want to scrape
BIZ_DICT, PROPS = get_biz_urls("Apartment Ratings")

logline = 79*'*'

class AptratingsSpider(CrawlSpider):
    '''
    Spider for crawling Apartment Ratings and extracting ratings data
    http://readthedocs.org/docs/scrapy/en/latest/topics/spiders.html?highlight=crawlspider
    TODO - dump spider stats into json file in pipelines

    To activate the spider from the command line type:
    >>> cd fever
    >>> cd apps/webcrawlers/feverbot
    >>> scrapy crawl AptratingsSpider
    '''
    name = 'AptratingsSpider'
    allowed_domain = ['98.158.196.12']

    start_urls = PROPS.keys()
    log.msg('Initializing Scrapy Rules \n', log.INFO)

    # Extract only from Austin and Cedar-Park
    rules = (
        Rule(SgmlLinkExtractor(
            allow=r'.*/rate/TX-(Austin|Cedar-Park).*-[0-9]+\.html',
            restrict_xpaths='//table[@class="opinTable"]',
            unique=True,
            process_value=lambda x: urljoin('98.158.196.12', x.strip()) ),
            follow=True,
            callback='parse_reviewpg'),
    )

    def parse_start_url(self, response):
        '''Scrape the homepage of an apartment
        '''
        log.msg(logline, log.INFO)
        log.msg('PARSING HOME PAGE', log.INFO)
        log.msg(logline+'\n', log.INFO)

        hxs    = HtmlXPathSelector(response)
        biz_id = PROPS[response.url]
        homepg = Apt()

        # get the Django biz.id for the apartment whose data your scraping
        homepg['biz_id'] = biz_id

        # collect the main rating & percentage
        homepg['recommended_by'] = float(
            hxs.select('//span[@class="reco"]/text()')[0].extract().strip('%'))
        homepg['total_overall_rating'] = float(
            hxs.select('//div[@class="ratingNum"]/div[@class="rating"]/text()')[0].extract().strip('%'))

        # get the table that holds the apartment ratings review data
        ratings = hxs.select('//table[@class="opinTable"]')

        # get the individual fields (parking, maintenance, noise, grounds, etc)
        # example output: ['3.8', 'Parking', '3.6', 'Maintenance', ...]
        rs = [x.strip().lower() for x in \
            ratings.select('//div[@id="box2"]//text()[normalize-space()]').extract()]

        # for every 2nd item (the field title) replace it's spaces with
        # underscores and convert it's value to a float
        for i, name in enumerate(rs):
            if i % 2 == 1:
                key = "overall_"+name.replace(' ', '_').replace(':', '')
                homepg[key] = float(rs[i-1])
        #log.msg(homepg, log.INFO)
        return homepg

    def parse_reviewpg(self, response):
        '''Parses an individual review page
        '''
        log.msg(logline, log.INFO)
        log.msg('PARSING CUSTOMER REVIEW PAGE', log.INFO)
        log.msg(logline+'\n', log.INFO)

        hxs    = HtmlXPathSelector(response)
        review = AptReview()

        # get the URL and biz.id so that you can identify this apartment
        review['comment_url'] = response.url

        # all info on the page is contained w/in this item
        h = hxs.select('//div[@class="complexContent"]')

        # get title of post
        comment_title = h.select('div/div//h2/text()').extract()
        try:
            review['comment_title'] = comment_title[0].strip()
        except IndexError:
            log.msg('COULD NOT FIND A VALUE FOR review["comment_title"]', log.ERROR)
            review['comment_title'] = 'NONE'

        # get the div that holds comment poster information
        # from, date-posted, years-at-apt
        info = [x.strip() for x in \
                    h.select('div/div/text()').extract() if x.strip()]

        for line in info:
            # get username
            if line.startswith('From'):
                if 'Anonymous' in line:
                    review['comment_username'] = 'Anonymous'
                else:
                    review['comment_username'] = esc_chars(
                                      line.split('From:')[1])
            # get date comment was posted
            if line.startswith('Date posted'):
                review['comment_post_date'] = esc_chars(
                            line.split('Date posted:')[1])
            # get years poster spent at apartment
            if line.startswith('Years'):
                review['comment_years_stayed'] = esc_chars(
                   line.split('Years at this apartment:')[1])

        # get the message they left
        msg = h.select('child::div[position()=2]/p/text()').extract()
        review['comment_message'] = esc_chars(msg[0].strip())

        # get the date at which this comment was last edited
        # if there is no last_edit date, then catch with an exception
        # and save a value of NONE
        last_updated = h.select('child::div[position()=2]/p/span/text()').extract()
        try:
            last_updated = "".join(last_updated[0].split())
            review['last_edited'] = last_updated.split(":")[1]
        except IndexError:
            review['last_edited'] = 'NONE'

        #---------------------------------------------------------------------
        # REPLIES
        #---------------------------------------------------------------------

        # make a reply dict and extract all the text in the replies table
        reply     = autoViv()
        reply_txt = [esc_chars(x) for x in \
                        h.select('div/table//text()').extract() if x.strip()]

        # for each reply on the page, create a dict (id, name, date, message)
        # and add it to the master reply dictionary.
        j = 0
        for i, line in enumerate(reply_txt):
            if line == 'From:':
                j += 1
                reply[j]['reply_name'] = reply_txt[i+1].strip()

            if line == 'Date:':
                reply[j]['reply_date'] = reply_txt[i+1]
                try:
                    reply[j]['reply_msg'] = reply_txt[i+2]
                except IndexError:
                    log.msg('IndexError - reply[j]["reply_msg"] = line[i+2] FAILED', log.ERROR)
                    reply[j]['reply_msg'] = ''

        # store your replies dictionary, assuming one exists
        if reply:
            review['replies'] = reply

        #---------------------------------------------------------------------
        # RATINGS
        #---------------------------------------------------------------------

        # get the numerical rating (1-5) for each of the following labels
        labels = ('overall_rating', 'parking', 'maintenance', 'construction',
                                'noise', 'grounds', 'safety', 'office_staff')
        scores = [int(x[0]) for x in \
                h.select('//table[@id="reviewRatings"]//img[@alt]/@alt').extract()]

        # save each rating into their properly labeled item
        for i, label in enumerate(labels):
            review[label] = scores[i]

        return review


#-----------------------------------------------------------------------------
# TODO
#-----------------------------------------------------------------------------
"""
    - extend the items class so that you can add meta data.
      homepg.biz_name = BIZ_DICT[biz_id] # add current biz name
      see the following URL for details:
      http://doc.scrapy.org/en/latest/topics/items.html


htmlspaced = re.sub(r"\r\n", " ", html)

def remove_nondigits(s):
    # remove all non numerical characters from string
    return re.sub(r"[^0-9]", "", s)
"""

