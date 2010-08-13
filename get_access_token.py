#!/usr/bin/python2.4
#
# Copyright 2007 The Python-Twitter Developers
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


import os
import sys
import urlparse

import oauth2 as oauth

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

app_consumer_key    = None
app_consumer_secret = None

if app_consumer_key is None or app_consumer_secret is None:
  print 'You need to edit this script and provide values for the'
  print 'app_consumer_key and also app_consumer_secret'
  sys.exit(1)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
oauth_consumer             = oauth.Consumer(key=app_consumer_key, secret=app_consumer_secret)
oauth_client               = oauth.Client(oauth_consumer)

print 'Requesting temp token from Twitter'

resp, content = oauth_client.request(REQUEST_TOKEN_URL, 'GET')

if resp['status'] != '200':
  print 'Invalid respond from Twitter requesting temp token: %s' % resp['status']
else:
  request_token = dict(urlparse.parse_qsl(content))

  print ''
  print 'Please visit this Twitter page and retrieve the pincode to be used'
  print 'in the next step to obtaining an Authentication Token:'
  print ''
  print '%s?oauth_token=%s' % (AUTHORIZATION_URL, request_token['oauth_token'])
  print ''

  pincode = raw_input('Pincode? ')

  token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
  token.set_verifier(pincode)

  print ''
  print 'Generating and signing request for an access token'
  print ''

  oauth_client  = oauth.Client(oauth_consumer, token)
  resp, content = oauth_client.request(ACCESS_TOKEN_URL, method='POST', body='oauth_verifier=%s' % pincode)
  access_token  = dict(urlparse.parse_qsl(content))

  if resp['status'] != '200':
    print 'The request for a Token did not succeed: %s' % resp['status']
    print access_token
  else:
    print 'Your Twitter Access Token key: %s' % access_token['oauth_token']
    print '                       secret: %s' % access_token['oauth_token_secret']
    print ''

