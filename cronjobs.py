#!/usr/bin/python

import constants
import fbgraph
import lastfm
import nikeplus
import re
import subprocess
import sys

services = ["last.fm", "nikeplus"]

class CrontabLine:
    def __init__(self, line=None, hour=None, dayofweek=None, command=None,
                 fb_id=None, username=None, service=None):
        if line:
            fields = line.split(" ")
            self.hour = int(line[1])
            self.dayofweek = int(line[4])
            self.command = " ".join(line[5:-3])
            self.fb_id = line[-3]
            self.username = line[-2]
            self.service = line[-1]
        else:
            self.hour = int(hour)
            self.dayofweek = int(dayofweek)
            self.command = command
            self.fb_id = fb_id
            self.username = username
            self.service = service
    def __repr__(self):
        return "* %d * * %d %s %s %s %s\n" % (self.hour, self.dayofweek,
                                              self.command, self.fb_id,
                                              self.username, self.service)

def add_cron_job(fb_id, day_of_week, hour, username, service):
    if service not in services:
        return
    if day_of_week < 0 or day_of_week > 6 or hour < 0 or hour > 23:
        return
    if not re.match("^[0-9]*$", fb_id):
        return
    if not re.match("^[0-9a-zA-Z_]*$", username):
        return
    line = CrontabLine(hour=hour, dayofweek=day_of_week,
                       command=constants.CRONJOB_COMMAND, fb_id=fb_id,
                       username=username, service=service)
    with open(constants.CRONTAB_FILE, "a") as f:
        f.write(repr(line))
    subprocess.call(["crontab", constants.CRONTAB_FILE])

def remove_cron_jobs(fb_id):
    if not re.match("^[0-9]*$", fb_id):
        return
    with open(constants.CRONTAB_FILE, "w+") as f:
        lines = f.readlines()
        final_lines = []
        for l in lines:
            try:
                c_line = CrontabLine(line=l)
            except ValueError:
                continue
            if c_line.fb_id != fb_id:
                final_lines.append(l)
        f.writelines(final_lines)
    subprocess.call(["crontab", constants.CRONTAB_FILE])
    
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
    elif sys.argv[3] == "nikeplus":
        distance = nikeplus.get_weekly_run_total(sys.argv[2])
        fbgraph.post_to_user_feed(sys.argv[1], nikeplus.get_weekly_evaluation(distance))
