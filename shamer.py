#!/usr/bin/python

import constants
import cronjobs
import fbgraph
import shamerdb
import urllib
import web

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
            if not shamerdb.get_user_by_fb_id(user_dict["id"]):
                shamerdb.create_user(user_dict["id"],
                                     user_dict["name"],
                                     user_dict["first_name"],
                                     user_dict["last_name"],
                                     access_token)
            return render.index(None, user_dict["id"], user_dict["first_name"])
        else:
            auth_url = constants.FB_OAUTH_DIALOG_URL + urllib.urlencode(
                 {"client_id": constants.FB_APP_ID,
                  "redirect_uri": constants.FB_REDIRECT_URI,
                  "scope": "publish_stream,offline_access"})
            return render.index(auth_url, None, None)

class change_options:
    def POST(self):
        i = web.input(fb_id=None, lastfmcheckbox=None,
                      lastfmusername=None, dayofweek=None,
                      hour=None, deleteinfo=None)
        if not i.fb_id:
            raise web.seeother('/')
        if i.deleteinfo:
            shamerdb.delete_user_by_fb_id(i.fb_id)
            raise web.seeother('/')
        d, h = None, None
        if i.dayofweek != None and i.hour != None:
            try:
                d = int(i.dayofweek)
                h = int(i.hour)
            except ValueError:
                raise web.seeother('/')
            if 0 <= d and d <= 6 and 0 <= h and h <= 23:
                shamerdb.set_user_reminder_time(i.fb_id, d, h)
            else:
                raise web.seeother('/')
        if i.lastfmcheckbox == "True" and i.lastfmusername:
            shamerdb.set_user_last_fm_pref(i.fb_id, True, i.lastfmusername)
            if d and h:
                cronjobs.add_cron_job(i.fb_id, d, h,
                                      i.lastfmusername, "last.fm")
        else:
            shamerdb.set_user_last_fm_pref(i.fb_id, False, "")
        return render.optionsset()
            
if __name__ == "__main__":
    shamerdb.database_init()
    app.run()
