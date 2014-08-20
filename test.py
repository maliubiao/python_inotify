#! /usr/bin/env python
import os 
import time
import _inotify 

def rev(event):
    print event

fd = _inotify.create()
wd = _inotify.add(fd, "test", _inotify.ALL_EVENTS);

while True:
    time.sleep(0.5)
    _inotify.read_event(fd, rev_event)

