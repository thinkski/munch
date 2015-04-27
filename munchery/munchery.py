"""Munch : A programmatic interface to Munchery.com"""

import json
import re
import urllib
import urllib2
import sys
from cookielib import CookieJar

from bs4 import BeautifulSoup


#    response = opener.open('https://munchery.com')
#    soup = BeautifulSoup(response.read())
#    tag = soup.find('meta', attrs={'name': 'csrf-token'})
#    csrf_token = tag['content']

class UnsupportedZipCode(Exception):

    def __init__(self):
        self.msg = 'Munchery does not deliver to this zip code'


class Munchery(object):

    def __init__(self):
        cj = CookieJar()
        self.opener_ = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    def set_zipcode(self, zipcode):
        """Set the postal zip code

        Munchery.com requires user to specify a postal code before it allows
        the user to view the menu as menus are region specific. This code is
        stored in a cookie. This function sets our zip code via an API POST
        request, which in turn sets our cookie.

        Arguments:
            zipcode : (string) Five digit zip code
        """
        url = "https://munchery.com/api/cart/set_address"
        data = json.dumps({
            "address": {
                "zipcode": zipcode
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            request = urllib2.Request(url, data, headers)
            response = self.opener_.open(request)
        except urllib2.HTTPError as e:
            # 400 Bad Request returned when Munchery does not deliver here
            if e.code == 400:
                raise UnsupportedZipCode
            else:
                raise e

    def get_menu(self):
        """Get menu"""
        url = "https://munchery.com/menus/sf/"
        request = urllib2.Request(url)
        response = self.opener_.open(request)

        # Parse response. Munchery uses Angular.js, thus full menu is available
        # within javascript.
        soup = BeautifulSoup(response.read())
        tag = soup.find('script', attrs={'class': 'menu-page-data'})

        return json.loads(tag.text)
