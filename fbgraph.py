#!/usr/bin/python

import urllib
import urllib2
import urlparse

APP_ID = ""
REDIRECT_URI = ""
APP_SECRET = ""

OAUTH_DIALOG_URL = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode({"client_id": APP_ID, "redirect_uri": REDIRECT_URI, "scope": "publish_stream,offline_access"})
ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token?"
CURRENT_USER_URL = "https://graph.facebook.com/me?"

def get_access_token(code):
    args = urllib.urlencode({"client_id": APP_ID, "redirect_uri": REDIRECT_URI, "client_secret": APP_SECRET, "code": i.code})
    access_url = ACCESS_TOKEN_URL + args
    response = urllib2.urlopen(access_url).read()
    response_dict = urlparse.parse_qs(response)
    return response_dict['access_token'][0]

def get_current_user_info(access_token):
    args = urllib.urlencode({"access_token", access_token})
    current_user_url = CURRENT_USER_URL + args
    response = urllib2.urlopen(current_user_url).read()
    return response
