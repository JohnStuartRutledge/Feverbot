
import sys, os, imp, datetime

#-----------------------------------------------------------------------------
# ACTIVATE DJANGO ENVIRONMENT
#-----------------------------------------------------------------------------

from django.core.management import setup_environ

MYAPP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if MYAPP_ROOT in sys.path:
    pass
else:
    sys.path.insert(0, MYAPP_ROOT)

os.environ['PYTHONPATH'] = MYAPP_ROOT
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
f, filename, desc = imp.find_module('settings', [MYAPP_ROOT])
settings = imp.load_module('settings', f, filename, desc)
setup_environ(settings)

from django.utils.dateformat import DateFormat
from myproject.apps.biz.models import Business, Website, WebsiteTypes

#-----------------------------------------------------------------------------
# HELPERS FOR FEVERBOT SPIDERS
#-----------------------------------------------------------------------------

current_time = datetime.datetime.now()
now = str(current_time)


class FeverException(Exception):
    pass

class autoViv(dict):
    """ Implementation of Perl-like auto-vivification feature
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def whitespaceBegone(s):
    '''Remove all whitespace from a string including space between words
    '''
    return "".join(s.split())

def replace_txt(txt, word_dic):
    '''Scan text for words that match a given key
    & replace them with the keys associated value.

    EXAMPLE USAGE:
    trans = {
        'a': 'x',
        'b': 'y',
        'c': 'z'
    }
    print replace_txt("a b c", trans)
    # 'x y z'
    '''
    rc = re.compile('|'.join(map(re.escape, word_dic)))
    def translate(match):
        return word_dic[match.group(0)]
    return rc.sub(translate, txt)


def str_to_unicode(text, encoding=None, errors='strict'):
    ''' Converts a string to unicode
    Function insipired by scrapy.W3lib
    '''
    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, str):
        return text.decode(encoding, errors)
    return text

def unicode_to_str(text, encoding=None, errors='strict'):
    ''' Converts unicode to a string
    Function insipired by scrapy.W3lib
    '''
    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, unicode):
        return text.encode(encoding, errors)
    return text

def replace_escape_chars(text, which_ones=('\n', '\t', '\r'), replace_by=u'', \
        encoding=None):
    """ Remove escape chars
    @which_ones - tuple of escape chars we want to remove. Default: \n, \t, \r
    @replace_by - txt you want to replace excaped chars with Default: ''
    """
    for ec in which_ones:
        text = text.replace(ec, str_to_unicode(replace_by, encoding))
    return str_to_unicode(text, encoding)

def make_filename(scraper_name, filetype):
    '''Creates a string to serve as the output name for the
    given filetype. e.g, the Yelp scraper with filetype=json
    would produce: 'YELP-2012-08-30T12:20:00.json'
    '''
    return current_time.strftime("".join(
        (scraper_name, "-%Y-%m-%dT%H-%M-%S.", filetype)))


def get_biz_urls(site_type):
    '''Takes the name of the site your scraping (e.g, Yelp, Facebook) and
    returns a dictionary of URLs to scrape along with their matching biz id
    EXAMPLE OUTPUT (key=url, val=biz.id):
    {u'http://www.apartmentratings.com/<APT-URL>.html': 3,
        ...
    }
    '''
    # create the list of websites to scrape by querying Django DB
    website_id = WebsiteTypes.objects.get(site_type=site_type).id
    results    = Website.objects.values('business', 'site_url').filter(site_type=website_id)
    BIZ_DICT   = {x['id']:x['biz_name'] for x in Business.objects.values('id', 'biz_name')}
    if results:
        PROPS = { x['site_url']: x['business'] for x in results if x['site_url'] }
    else:
        raise FeverException('No Matching Businesses were found in the Django Database')
    return BIZ_DICT, PROPS



