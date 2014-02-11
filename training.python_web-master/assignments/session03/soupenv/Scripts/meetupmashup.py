#this script scans (two) meetup pages for all upcoming events. It pulls all those events into one
#list, sorts them by date and time, and prints them. I wanted to crosscheck the dates against my
#Google callendar, or at least write some kind of comparison function to flag time conflicts,
#but this was a tough project and I didn't have time. This is definitely the most useful thing I've
#learned in either class though. Thanks!

from bs4 import BeautifulSoup
import requests
from datetime import datetime 
import time

def find_meetups(base):
    base = base
    resp = requests.get(base, timeout=5)
    resp.raise_for_status() #<- no-op if status==200
    return resp.content, resp.encoding


def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, from_encoding=encoding)
    return parsed

def extract_meetup(doc):
    eventsraw = doc.find_all('span', itemprop="summary")
    timeraw = doc.find_all('time', itemprop="startDate")
    events = []
    times = []
    for event in eventsraw:
        event = str(event)
        events.append(event[event.index('"summary">')+10:event.index('</span')])
    for time in timeraw:
        time = str(time)
        time = (time[time.index('e="')+3:time.index(':00-08')])
        times.append(datetime.strptime(time, "%Y-%m-%dT%H:%M"))
    return zip(events, times)


if __name__ == '__main__':
    html, encoding = find_meetups('http://www.meetup.com/seattlebluegrass/')
    doc = parse_source(html, encoding)
    bgmeetups = extract_meetup(doc)
    html, encoding = find_meetups('http://www.meetup.com/Story-Games-Seattle/')
    doc = parse_source(html, encoding)
    sgmeetups = extract_meetup(doc)
    for i in sgmeetups:
        bgmeetups.append(i)
    bgmeetups.sort(key=lambda tup: tup[1])
    for event in bgmeetups:
        event = list(event)
        print event[0], event[1].strftime("%Y-%m-%d %I:%M%p")

