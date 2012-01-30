#!/usr/bin/python

import web

APP_ID = ""
REDIRECT_URI = ""
OAUTH_DIALOG_URL = "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=publish_stream" % (APP_ID, REDIRECT_URI)

urls = (
    '/', 'index'
    )

app = web.application(urls, globals())
render = web.template.render('templates/')

class index:
    def GET(self):
        return render.index(AUTH_URL)

if __name__ == "__main__":
    app.run()
