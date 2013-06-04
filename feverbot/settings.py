# Scrapy settings for feverbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import random

#-----------------------------------------------------------------------------
# BOT INFO
#-----------------------------------------------------------------------------
BOT_NAME         = 'feverbot'
BOT_VERSION      = '1.0'
SPIDER_MODULES   = ['feverbot.spiders']
NEWSPIDER_MODULE = 'feverbot.spiders'
USER_AGENT       = "Feverbot"

#-----------------------------------------------------------------------------
# PIPELINES
#-----------------------------------------------------------------------------
ITEM_PIPELINES = ['feverbot.pipelines.FeverbotPipeline']
# ITEM_PIPELINES = ['feverbot.pipelines.FeverJsonPipeline']

#-----------------------------------------------------------------------------
# CONCURRENT
#-----------------------------------------------------------------------------
# only make one request at a time
CONCURRENT_REQUESTS_PER_DOMAIN = 3

# only run one spider at a time
CONCURRENT_SPIDERS = 1

#-----------------------------------------------------------------------------
# DELAY
#-----------------------------------------------------------------------------
# add a time delay to your downloads.
# random between 0 seconds and 1/4th a second
# DOWNLOAD_DELAY   = float("{0:.2f}".format(random.uniform(0, 0.25)))
DOWNLOAD_TIMEOUT = 720  # default: 180
DOWNLOADER_STATS = True
RANDOMIZE_DOWNLOAD_DELAY = True

#-----------------------------------------------------------------------------
# LOGS & STATS
#-----------------------------------------------------------------------------

LOG_ENABLED  = True
LOG_LEVEL    = 'DEBUG' # options: CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_FILE     = 'feverbot.log'
LOG_ENCODING = 'utf-8'

STATS_ENABLED = True
STATS_DUMP    = True  # default = False


'''
# Depth limit
DEPTH_LIMIT=10

MEMUSAGE_NOTIFY_MAIL = False
MEMUSAGE_REPORT      = False
MEMUSAGE_WARNING_MB  = 0

REDIRECT_MAX_TIMES = 20
SCHEDULER_ORDER    = 'DFO'   # DFO or BFO
'''

#-----------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------

"""
# uncomment this code if you want to use a random user agent per each request.

from scraper.settings import USER_AGENT_LIST
import random
from scrapy import log

class RandomuserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)
        # log.msg('>>>> UA %s' % request.headers)

# to use the above code you must add the following to this file

DOWNLOADER_MIDDLEWARES = {
    'scraper.randome_user_agent.RandomUserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

"""
