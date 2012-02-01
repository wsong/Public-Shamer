#!/usr/bin/python

import web
import fbgraph

urls = (
    '/', 'index'
    )

app = web.application(urls, globals())
render = web.template.render('templates/')

class index:
    def GET(self):
        i = web.input(code=None)
        if i.code:
            access_token = fbgraph.get_access_token(i.code)
            open(".access_token", "w").write(access_token)
            return render.index("")
        else:
            return render.index(OAUTH_DIALOG_URL)
            

if __name__ == "__main__":
    app.run()
