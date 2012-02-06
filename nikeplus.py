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
        "This week, I ran %.2f miles; that moving sidewalk I installed is basically paying for itself." % (distance),
        ]
    return random.choice(message_list)

def get_low_evaluation(distance):
    message_list = [
        "This week I ran %.2f miles, which is really not that much.  I mean, did I run on my hands or something?" % (distance),
        ]
    return random.choice(message_list)

def get_medium_low_evaluation(distance):
    message_list = [
        "Over the last seven days, I ran %.2f miles, which isn't exactly the distance from Marathon to Athens.  If we're being honest, it's really more like the distance from my apartment to the corner store." % (distance),
        ]
    return random.choice(message_list)

def get_medium_evaluation(distance):
    message_list = [
        "Over the last week, I ran %.2f miles.  Pretty respectable, I'd say; just a few more miles a week and I'll have justified my five-toed shoes purchase." % (distance),
        ]
    return random.choice(message_list)

def get_default_evaluation(distance):
    message_list = [
        "I ran %.2f miles this week.  If everyone was like me, we could solve the energy crisis by just running everywhere." % (distance),
        ]
    return random.choice(message_list)

def get_weekly_evaluation(distance):
    miles = distance*0.621371192
    if miles <= 1.0:
        return get_very_low_evaluation(miles)
    elif miles <= 3.0:
        return get_low_evaluation(miles)
    elif miles <= 7.0:
        return get_medium_low_evaluation(miles)
    elif miles <= 12.0:
        return get_medium_evaluation(miles)
    else:
        return get_default_evaluation(miles)
