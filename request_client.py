# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Sample application that demonstrates different ways of fetching
URLS on App Engine
"""

import logging
import urllib
import json
import numpy as np

# [START urllib2-imports]
import urllib2
# [END urllib2-imports]

# [START urlfetch-imports]
from google.appengine.api import urlfetch
# [END urlfetch-imports]
import webapp2


class UrlLibFetchHandler(webapp2.RequestHandler):
    """ Demonstrates an HTTP query using urllib2"""

    def get(self):
        # [START urllib-get]
        url = 'http://104.196.164.200'
        try:
            result = urllib2.urlopen(url)
            self.response.write(result.read())
        except urllib2.URLError:
            logging.exception('Caught exception fetching url')
        # [END urllib-get]


class UrlFetchHandler(webapp2.RequestHandler):
    """ Demonstrates an HTTP query using urlfetch"""

    def get(self):
        # [START urlfetch-get]
        url = 'http://104.196.164.200'
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                self.response.write(result.content)
            else:
                self.response.status_code = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
        # [END urlfetch-get]


class UrlPostHandler(webapp2.RequestHandler):
    """ Demonstrates an HTTP POST form query using urlfetch"""

    def get(self):
        # [START urlfetch-post]
        
        array = np.array([1,2,3]).tolist()
        jsonlist = json.dumps(array) # Converting to str type
        #logging.info(jsonlist)        
        
        form_fields = {
            'first_name': 'Albert',
            'last_name': jsonlist,
        }
        
        try:
            #form_data = urllib.urlencode(UrlPostHandler.form_fields)
            form_data = json.dumps(form_fields)   # Converting to str type
            #logging.info(form_data)            
            headers = {'Content-Type': 'application/json'}
            result = urlfetch.fetch(
                url='http://104.196.33.188/',
                payload=form_data,
                method=urlfetch.POST,
                headers=headers)
            self.response.write(result.content)
            #logging.info(result.content)
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
        # [END urlfetch-post]


class SubmitHandler(webapp2.RequestHandler):
    """ Handler that receives UrlPostHandler POST request"""

    def post(self):
        self.response.out.write((self.request.get('first_name')))


app = webapp2.WSGIApplication([
    ('/', UrlLibFetchHandler),
    ('/url_fetch', UrlFetchHandler),
    ('/url_post', UrlPostHandler),
    ('/submit_form', SubmitHandler)
], debug=True)