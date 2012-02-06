#!/usr/bin/python

import constants
import datetime
import random
import time
import urllib
import urllib2
from xml.dom import minidom

RETRIES = 5

def get_xml(u):
    for i in range(RETRIES):
        try:
            return minidom.parse(urllib2.urlopen(u))
        except IOError:
            print "Connection to last.fm failed."
        time.sleep(1)

# Note that Nike+ (and therefore this function) returns distances in
# kilometers, not miles
def get_weekly_run_total(user_id):
    url = constants.NIKE_PLUS_URL + urllib.urlencode({"userID": user_id})
    runs_xml = get_xml(url)
    if runs_xml.getElementsByTagName("status")[0].firstChild.nodeValue == "failure":
        raise IOError("Could not get Nike+ data; userID may be invalid")
    last_week_dates = [str(datetime.date.today() - datetime.timedelta(days=i)) for i in range(7)]
    runs = runs_xml.getElementsByTagName("run")
    total = 0.0
    for node in runs:
        start_time = node.getElementsByTagName("startTime")[0].firstChild.nodeValue
        if start_time[:10] in last_week_dates:
            total += float(node.getElementsByTagName("distance")[0].firstChild.nodeValue)
    return total

def get_very_low_evaluation(distance):
    message_list = [
        "This week, I ran %d miles; that moving sidewalk I installed is basically paying for itself." % (distance),
        ]
    return random.choice(message_list)

def get_default_evaluation(distance):
    message_list = [
        "I ran %d miles this week.  If everyone was like me, we could solve the energy crisis by just running everywhere." % (distance),
        ]
    return random.choice(message_list)

def get_weekly_evaluation(distance):
    miles = distance*0.621371192
    if miles <= 1:
        return get_very_low_evaluation(miles)
    else:
        return get_default_evaluation(miles)
