#!/usr/bin/python

import web
import fbgraph
import shamerdb

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
            user_dict = fbgraph.get_current_user_info(access_token)
            if not shamerdb.get_user_by_fb_id(user_dict["id"][0]):
                shamerdb.create_user(user_dict["id"][0],
                                     user_dict["name"][0],
                                     user_dict["first_name"][0],
                                     user_dict["last_name"][0],
                                     access_token)
            return render.index("")
        else:
            return render.index(OAUTH_DIALOG_URL)
            

if __name__ == "__main__":
    shamerdb.database_init()
    app.run()
