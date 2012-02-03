#!/usr/bin/python

import constants
import json
import shamerdb
import urllib
import urllib2
import urlparse

# Performs a GET request to get the access token of a certain user.  The code
# comes from Facebook's servers after the user has approved our app.
def get_access_token(code):
    args = urllib.urlencode({"client_id": constants.FB_APP_ID,
                             "redirect_uri": constants.FB_REDIRECT_URI,
                             "client_secret": constants.FB_APP_SECRET,
                             "code": code})
    access_url = constants.FB_ACCESS_TOKEN_URL + args
    response = urllib2.urlopen(access_url).read()
    response_dict = urlparse.parse_qs(response)
    return response_dict['access_token'][0]

# Performs a GET request to get the info of the user who owns this access token.
# Returns a dictionary of their info (name, Facebook ID, etc.).
def get_current_user_info(access_token):
    args = urllib.urlencode({"access_token": access_token})
    current_user_url = constants.FB_CURRENT_USER_URL + args
    response = urllib2.urlopen(current_user_url).read()
    return json.loads(response)

def post_to_user_feed(fb_id, message):
    user_row = shamerdb.get_user_by_fb_id(fb_id)
    if not user_row:
        return
    access_token = user_row["Access_Token"]
    data = urllib.urlencode({"access_token": access_token,
                             "message": message})
    urllib2.urlopen(constants.FB_FEED_URL, data)
