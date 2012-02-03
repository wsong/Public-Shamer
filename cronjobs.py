#!/usr/bin/python

import fbgraph
import lastfm
import re
import subprocess
import sys

CRONTAB_FILE = "/home/ec2-user/shamer-crontab"
commands = {"last.fm": "python /home/ec2-user/Public-Shamer/cronjobs.py"}

services = ["last.fm"]

def add_cron_job(fb_id, day_of_week, hour, username, service):
    if service not in commands:
        return
    if day_of_week < 0 or day_of_week > 6 or hour < 0 or hour > 23:
        return
    if not re.match("^[0-9]*$", fb_id):
        return
    if not re.match("^[0-9a-zA-Z_]*$", username):
        return
    command = commands[service] + " %s %s %s" % (fb_id, username, service)
    s = "* %d * * %d %s\n" % (hour, day_of_week, command)
    with open(CRONTAB_FILE, "a") as f:
        f.write(s)
    subprocess.call(["crontab", CRONTAB_FILE])
    
if __name__ == "__main__":
    # Usage: cronjobs facebook_id username service
    # facebook_id is the user's facebook ID
    # username is their username for their chosen service (e.g. last.fm)
    # service is the name of a service (again, like "last.fm")
    if len(sys.argv) != 4:
        print "Usage: cronjobs facebook_id username service"
        sys.exit(1)
    if sys.argv[3] not in services:
        print "Service " + sys.argv[3] + " not supported."
        sys.exit(1)
    if sys.argv[3] == "last.fm":
        playcount = lastfm.get_lastfm_weekly_playcount(sys.argv[2])
        fbgraph.post_to_user_feed(sys.argv[1], lastfm.get_weekly_evaluation(playcount))
