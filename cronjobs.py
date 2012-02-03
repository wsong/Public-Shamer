#!/usr/bin/python

import lastfm
import subprocess
import sys

CRONTAB_FILE = "/home/ec2-user/shamer-crontab"
LAST_FM_COMMAND = "python /home/ec2-user/Public-Shamer/cronjobs.py"

services = ["last.fm"]

def add_lastfm_cron_job(day_of_week, hour, lastfm_username):
    if day_of_week < 0 or day_of_week > 6 or hour < 0 or hour > 23:
        return
    s = "* %d * * %d %s\n" % (hour, day_of_week, LAST_FM_COMMAND)
    with open(CRONTAB_FILE, "a") as f:
        f.write(s)
    subprocess.call(["crontab", CRONTAB_FILE])
    
if __name__ = "__main__":
    # Usage: cronjobs facebook_id username service
    # facebook_id is the user's facebook ID
    # username is their username for their chosen service (e.g. last.fm)
    # service is the name of a service (again, like "last.fm")
    if len(sys.argv) != 4:
        print "Usage: cronjobs facebook_id username service"
        return
    if sys.argv[3] not in services:
        print "Service " + sys.argv[3] + " not supported."
        return
    if method == "last.fm":
        playcount = lastfm.get(get_lastfm_weekly_playcount(sys.argv[2]))
        post_to_user_feed(sys.argv[1], lastfm.get_weekly_evaluation(playcount))
