#!/usr/bin/python

import constants
import time
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

def get_lastfm_weekly_playcount(user):
    url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user=%s&api_key=%s&period=7day' % (user, constants.LASTFM_API_KEY)
    tracks = get_xml(url).getElementsByTagName("track")
    total = 0
    for node in tracks:
        total += int(node.getElementsByTagName("playcount")[0].firstChild.nodeValue)
    return total

def get_weekly_evaluation(count):
    if count <= 10:
        return "I listened to %d songs this week, which is just breathtakingly low.  My top three artists are the Beatles, Linkin Park, and, hrm, the last one is a tie between the Eagles and... did I already say the Beatles?" % (count)
    elif count <= 20:
        return "I listened to %d songs this week, which is like a single album.  Well, if you count %d repetitions of \"Like a G6\" as an album." % (count, count)
    elif count <= 40:
        return "I listened to %d songs this week, which is so close to being a good length of music (unless it's %d Dream Theater songs, in which case I guess I listened to like %d hours of music)." % (count, count, count*3)
    elif count <= 70:
        return "I listened to %d songs this week; sounds like I had a good time (oh no my social life D:)." % (count)
    else:
        return "On the downside, I was never able to take my headphones out this week.  On the upside, I listened to %d songs." % (count)
