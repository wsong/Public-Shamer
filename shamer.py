#!/usr/bin/python

import web
import fbgraph
import shamerdb

urls = (
    '/', 'index',
    '/change_options/', 'change_options'
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
            return render.index(None, user_dict["id"], user_dict["first_name"])
        else:
            return render.index(fbgraph.OAUTH_DIALOG_URL, None, None)

class change_options:
    def POST(self):
        print "yay"
        i = web.input(fb_id=None, lastfmcheckbox=None, dayofweek=None,
                      hour=None, deleteinfo=None)
        if not i.fb_id:
            raise web.seeother('/')
        if i.deleteinfo:
            shamerdb.delete_user_by_fb_id(fb_id)
            raise web.seeother('/')
        if i.lastfmcheckbox == "True":
            shamerdb.set_user_last_fm_pref(fb_id, True)
        else:
            shamerdb.set_user_last_fm_pref(fb_id, False)
        if i.dayofweek != None and i.hour != None:
            d = None
            h = None
            try:
                d = int(i.dayofweek)
                h = int(i.hour)
            except ValueError:
                raise web.seeother('/')
            if 0 <= d and d <= 6 and 0 <= h and h <= 23:
                shamerdb.set_user_reminder_time(fb_id, d, h)
            else:
                raise web.seeother('/')                
        return render.optionsset()
            
if __name__ == "__main__":
    shamerdb.database_init()
    app.run()
