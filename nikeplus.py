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
