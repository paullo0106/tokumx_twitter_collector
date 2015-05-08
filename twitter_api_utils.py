__author__ = 'Paul Lo'
__date__ = '2015-04-15'

import oauth2 as oauth
import urllib2 as urllib
import twitter_api_settings as settings


_debug = 0

oauth_token = oauth.Token(key=settings.ACCESS_TOKEN_KEY, secret=settings.ACCESS_TOKEN_SECRET)
oauth_consumer = oauth.Consumer(key=settings.API_KEY, secret=settings.API_SECRET)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


request_template = "https://api.twitter.com/1.1/search/tweets.json?q={}"


def send_search_request(search_term):
    """ Get the latest tweets containing keyword search_term

    :param search_term: keyword we want to search on twitter
    :type search_term: str
    """
    request_url = request_template.format(search_term)
    return twitterreq(request_url, 'GET', list())


def twitterreq(url, method, parameters):
    """Construct, sign, and open a twitter request
    """

    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                 token=oauth_token,
                                                 http_method=http_method,
                                                 http_url=url,
                                                 parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    #headers = req.to_header()
    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response
