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
        code = None
        if i.code:
            code = i.code
            web.setcookie("fb_code", i.code)
        else:
            code = web.cookies().get("fb_code")
        if code:
            access_token = fbgraph.get_access_token(code)
            user_dict = fbgraph.get_current_user_info(access_token)
            if not shamerdb.get_user_by_fb_id(user_dict["id"]):
                shamerdb.create_user(user_dict["id"],
                                     user_dict["name"],
                                     user_dict["first_name"],
                                     user_dict["last_name"],
                                     access_token)
                return render.index(fb_id=user_dict["id"],
                                    fb_first_name=user_dict["first_name"],
                                    dayofweek_menu=get_day_of_week_menu(0),
                                    hour_menu=get_hour_menu(0))
            else:
                user_row = shamerdb.get_user_by_fb_id(user_dict["id"])
                dayofweek_menu = get_day_of_week_menu(
                    user_row["Reminder_Time_Day_Of_Week"])
                hour_menu = get_hour_menu(user_row["Reminder_Time_Hour"])
                return render.index(fb_id=user_row["Facebook_Id"],
                                    fb_first_name=user_row["First_Name"],
                                    lastfm_pref=user_row["LastFm"],
                                    lastfm_username=user_row["LastFm_Username"],
                                    dayofweek_menu=dayofweek_menu,
                                    hour_menu=hour_menu)
        else:
            auth_url = constants.FB_OAUTH_DIALOG_URL + urllib.urlencode(
                 {"client_id": constants.FB_APP_ID,
                  "redirect_uri": constants.FB_REDIRECT_URI,
                  "scope": "publish_stream,offline_access"})
            return render.index(oauth_dialog_url=auth_url)

class change_options:
    def POST(self):
        i = web.input(fb_id=None, lastfmcheckbox=None,
                      lastfmusername=None, dayofweek=None,
                      hour=None, deleteinfo=None)
        if not i.fb_id:
            raise web.seeother('/')
        if i.deleteinfo:
            cronjobs.remove_cron_jobs(i.fb_id)
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
                cronjobs.remove_cron_jobs(i.fb_id)
                cronjobs.add_cron_job(i.fb_id, d, h,
                                      i.lastfmusername, "last.fm")
        else:
            shamerdb.set_user_last_fm_pref(i.fb_id, False, "")
        return render.optionsset()

def get_day_of_week_menu(default_value):
    return web.form.Dropdown(name="dayofweek",
                             args=[(0,"Sunday"), (1,"Monday"), (2,"Tuesday"),
                                   (3,"Wednesday"), (4,"Thursday"),
                                   (5,"Friday"), (6,"Saturday")],
                             value=default_value)

def get_hour_menu(default_value):
    return web.form.Dropdown(name="hour",
                             args=[(0, '12:00am'), (1, '1:00am'),
                                   (2, '2:00am'), (3, '3:00am'),
                                   (4, '4:00am'), (5, '5:00am'),
                                   (6, '6:00am'), (7, '7:00am'),
                                   (8, '8:00am'), (9, '9:00am'),
                                   (10, '10:00am'), (11, '11:00am'),
                                   (12, '12:00pm'), (13, '1:00pm'),
                                   (14, '2:00pm'), (15, '3:00pm'),
                                   (16, '4:00pm'), (17, '5:00pm'),
                                   (18, '6:00pm'), (19, '7:00pm'),
                                   (20, '8:00pm'), (21, '9:00pm'),
                                   (22, '10:00pm'), (23, '11:00pm')],
                             value=default_value)
    
if __name__ == "__main__":
    shamerdb.database_init()
    app.run()
