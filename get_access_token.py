#!/usr/bin/env python
#
# Copyright 2007-2013 The Python-Twitter Developers
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

# parse_qsl moved to urlparse module in v2.6
try:
    from urlparse import parse_qsl
except:
    from cgi import parse_qsl

import webbrowser
import oauth2 as oauth

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twittercongress.settings")
from congress_app.models import Twitter_FTV, Politician

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'
CONSUMER_KEY = 'hNxtR1bjU2QnJqQZYftUzA'
CONSUMER_SECRET = 'nXVHf7tiGzVvfrGA3VRSbdvjIIt1H706tjiP9rK2o4'

''' Gets access key and token for the Twitter user currently logged into default browser '''
def get_access_token(consumer_key, consumer_secret):

    signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
    oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    oauth_client = oauth.Client(oauth_consumer)

    print 'Requesting temp token from Twitter'

    resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'POST', body="oauth_callback=oob")

    if resp['status'] != '200':
        print 'Invalid respond from Twitter requesting temp token: %s' % resp['status']
    else:
        request_token = dict(parse_qsl(content))
        url = '%s?oauth_token=%s' % (AUTHORIZATION_URL, request_token['oauth_token'])

        print ''
        print 'I will try to start a browser to visit the following Twitter page'
        print 'if a browser will not start, copy the URL to your browser'
        print 'and retrieve the pincode to be used'
        print 'in the next step to obtaining an Authentication Token:'
        print ''
        print url
        print ''

        webbrowser.open(url)
        pincode = raw_input('Pincode? ')

        token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        token.set_verifier(pincode)

        print ''
        print 'Generating and signing request for an access token'
        print ''

        oauth_client = oauth.Client(oauth_consumer, token)
        resp, content = oauth_client.request(ACCESS_TOKEN_URL, method='POST', body='oauth_callback=oob&oauth_verifier=%s' % pincode)
        access_token = dict(parse_qsl(content))

        if resp['status'] != '200':
            print 'The request for a Token did not succeed: %s' % resp['status']
            print access_token
        else:
            print 'Your Twitter Access Token key: %s' % access_token['oauth_token']
            print '          Access Token secret: %s' % access_token['oauth_token_secret']
            print ''
            return access_token['oauth_token'], access_token['oauth_token_secret']

def main():
    # Check to see if Twitter_FTV model exists, or else create
    handle = raw_input('Twitter_FTV handle: ')
    try:
        twitter_ftv = Twitter_FTV.objects.get(handle=handle)
    except:
        # Identify desired politician to link account to
        print "Model does not yet exist. Please enter additional info to create:"
        last_name = raw_input('Last name of politician: ')
        politicians = Politician.objects.filter(last_name__contains=last_name)
        if len(politicians) == 0:
            print "No politicians found, please try again"
            return
        elif len(politicians) == 1:
            p_id = politicians[0].id
        else:  
            for p in politicians:
                print "%s %s: ID %s" % (p.first_name, p.last_name, p.id)
            p_id = raw_input('ID of correct politician (see above): ')

        # Finally create the account
        try: 
            print p_id
            twitter_ftv = Twitter_FTV.objects.create(handle=handle, politician_id=p_id)
            print 'Model successfully created'
        except:
            'Model could not be created'
            return

    
    # Check for other, non-necessary fields
    if not twitter_ftv.email:
        email = raw_input('Email address (return to bypass): ')
        twitter_ftv.email = email
    if not twitter_ftv.email_password:
        email_password = raw_input('Password (return to bypass): ')
        twitter_ftv.email_password = email_password
    twitter_ftv.save()

    # OAuth
    print 'Connecting to Twitter'
    if not consumer_key: 
        consumer_key = raw_input('Enter your consumer key: ')
    if not consumer_secret:
        consumer_secret = raw_input("Enter your consumer secret: ")
    access_key, access_secret = get_access_token(consumer_key, consumer_secret)
    twitter_ftv.access_key = access_key
    twitter_ftv.access_secret = access_secret
    twitter_ftv.save()

    # TODO: get twitter account id
    print 'Model successfully authed with Twitter!'


if __name__ == "__main__":
    main()