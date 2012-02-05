#!/usr/bin/python

import constants
import random
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

def get_very_low_evaluation(count):
    message_list = [
        "I listened to %d songs this week, which is just breathtakingly low.  Myn top three artists are the Beatles, Linkin Park, and, hrm, the last one is a tie between the Eagles and... did I already say the Beatles?" % (count),
        "This week, I listened to %d songs.  Kinda makes you wonder if I actually enjoy music, or if I just like the way earbuds feel." % (count),
        "Over the last seven days, I listened to %d songs.  I'm not actually into music, but I bought this iPod to look cooler on the subway and damned if I'm not using it." % (count),]
    return random.choice(message_list)

def get_low_evaluation(count):
    message_list = [
        "I listened to %d songs this week, which is like a single album.  Well, if you count %d repetitions of \"Like a G6\" as an album." % (count, count),
        "I, like, totally had LMFAO stuck in my head this week, and I listened to them like %d times." % (count),
        "I listened to %d song this week.  I would've listened to more, but NPR only publishes so many songs." % (count),]
    return random.choice(message_list)

def get_medium_low_evaluation(count):
    message_list = [
        "I listened to %d songs this week, which is so close to being a good length of music (unless it's %d Dream Theater songs, in which case I guess I listened to like %d hours of music)." % (count, count, count*3),
        "This week, I listened to %d songs.  I wanna listen to more music, but it's so hard to afford it all on iTunes.  99 cents is expensive!" % (count),
        "Over the last seven days, I listened to %d songs.  I'm really into music, but sometimes I wonder if what I'm really into is sounding like I'm into music." % (count),]
    return random.choice(message_list)

def get_medium_evaluation(count):
    message_list = [
        "I listened to %d songs this week; sounds like I had a good time (oh no my social life D:)." % (count),
        "I listened to %d songs over the last seven days; I'm really into Grizzly Bear, Ariel Pink, Wavves and... oh God, all my Pitchfork references are out of date." % (count),
        "Over the last seven days, I listened to %d songs; more or less where I wanna be in my listening career (well, except that %d of those were dubstep)." % (count, count),]
    return random.choice(message_list)

def get_default_evaluation(count):
    message_list = [
        "On the downside, I was never able to take my headphones out this week.  On the upside, I listened to %d songs." % (count),]
    return random.choice(message_list)

    
def get_weekly_evaluation(count):
    if count <= 10:
        return get_very_low_evaluation(count)
    elif count <= 20:
        return get_low_evaluation(count)
    elif count <= 40:
        return get_medium_low_evaluation(count)
    elif count <= 70:
        return get_medium_evaluation(count)
    else:
        return get_default_evaluation(count)
