# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
from scrapy.item import Item, Field

#-----------------------------------------------------------------------------
# YELP
#-----------------------------------------------------------------------------
class Yelp(Item):
    '''Class for holding Yelp data for a
    particular businesses Yelp profile'''
    biz_id       = Field()
    timestamp    = Field()
    stars        = Field()
    review_count = Field()
    # created_by = updated_by = -2    # feverbot
    # created_on
    # updated_on
    def __str__(self):
        return """Yelp: stars={0}, review_count={1}""".format(
            self['stars'], self['review_count'])


class YelpSimilar(Item):
    '''Class for holding data on which businesses Yelp marked
    as being similar to our currently selected business.'''
    similar_name         = Field()
    similar_link         = Field()
    similar_stars        = Field()
    similar_neighborhood = Field()

    def __str__(self):
        return """YelpSimilar: similar_name={0}, similar_link={1},
        similar_stars={2}, similar_neighborhood={3}""".format(
            self['similar_name'], self['similar_link'],
            self['similar_stars'], self['similar_neighborhood'])


class YelpReviews(Item):
    '''Class for holding all data specific to each individual
    review on a businesses Yelp page.'''
    # TODO
    # user_name
    # date_posted
    # stars
    # review_link
    # friend_count
    # review_count
    # photo_count
    # checkin_count
    # useful_count
    # funny_count
    # cool_count
    # message
    # timestamp
    pass

#-----------------------------------------------------------------------------
# APARTMENT RATINGS
#-----------------------------------------------------------------------------

class Apt(Item):
    '''Class for holding data specific to apartmentratings.com
    '''
    biz_id                 = Field()
    recommended_by         = Field(default=-1)
    total_overall_rating   = Field(default=-1)
    overall_parking        = Field(default=-1)
    overall_maintenance    = Field(default=-1)
    overall_construction   = Field(default=-1)
    overall_noise          = Field(default=-1)
    overall_grounds        = Field(default=-1)
    overall_safety         = Field(default=-1)
    overall_office_staff   = Field(default=-1)

    def __str__(self):
        return """Apt({0}): recommended_by={1}, rating={2}%""".format(
            self['biz_id'],
            self['recommended_by'],
            self['total_overall_rating'])


class AptReview(Item):
    '''Class for holding Individual review pages on apartmentratings.com
    this includes, user comments, user ratings, and any Replies
    '''
    comment_url          = Field()
    comment_title        = Field(default="untitled")
    comment_username     = Field()
    comment_post_date    = Field()
    comment_years_stayed = Field()
    comment_message      = Field()
    last_edited          = Field(default="unknown")
    replies              = Field(default="NONE")
    overall_rating       = Field(default=-1)
    parking              = Field(default=-1)
    maintenance          = Field(default=-1)
    construction         = Field(default=-1)
    noise                = Field(default=-1)
    grounds              = Field(default=-1)
    safety               = Field(default=-1)
    office_staff         = Field(default=-1)

    def __str__(self):
        return """AptReview: user={0}, title={1}""".format(
            self['comment_username'],
            self['comment_title'])


#-----------------------------------------------------------------------------
# CRAIGS LIST
#-----------------------------------------------------------------------------

class CraigsListItem(Item):
    '''Class for holding content scraped from Craigslist
    '''
    page_url = Field()
    img_urls = Field()

    def __str__(self):
        return """CraigsListItem: {0}""".format(self['page_url'])

