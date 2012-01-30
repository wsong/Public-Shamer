#!/usr/bin/python

import web
import urllib2
import urlparse

APP_ID = ""
REDIRECT_URI = ""
APP_SECRET = ""
OAUTH_DIALOG_URL = "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=publish_stream,offline_access" % (APP_ID, REDIRECT_URI)
ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s" % (APP_ID, REDIRECT_URI, APP_SECRET)

urls = (
    '/', 'index'
    )

app = web.application(urls, globals())
render = web.template.render('templates/')

class index:
    def GET(self):
        i = web.input(code=None)
        if i.code:
            access_url = ACCESS_TOKEN_URL + "&code=%s" % (i.code)
            response = urllib2.urlopen(access_url).read()
            response_dict = urlparse.parse_qs(response)
            access_token = response_dict['access_token'][0]
            open(".access_token", w).write(access_token)
            return render.index("")
        else:
            return render.index(OAUTH_DIALOG_URL)
            

if __name__ == "__main__":
    app.run()
