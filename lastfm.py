#!/usr/bin/python

from xml.dom import minidom
from urllib import urlopen
from time import sleep

RETRIES = 5

def get_xml(u):
    for i in range(RETRIES):
        try:
            return minidom.parse(urlopen(u))
        except IOError:
            print "Connection to last.fm failed."
        sleep(1)

def getLastFmWeeklyPlayCount(user, api_key):
    url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user=%s&api_key=%s&period=7day' % (user, api_key)
    tracks = get_xml(url).getElementsByTagName("track")
    total = 0
    for node in tracks:
        total += int(node.getElementsByTagName("playcount")[0].firstChild.nodeValue)
    return total
