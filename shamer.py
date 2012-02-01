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
                shamerdb.create_user(user_dict["id"],
                                     user_dict["name"],
                                     user_dict["first_name"],
                                     user_dict["last_name"],
                                     access_token)
            return render.index(None, user_dict["first_name"])
        else:
            return render.index(fbgraph.OAUTH_DIALOG_URL, None)
            

if __name__ == "__main__":
    shamerdb.database_init()
    app.run()
