#! /usr/bin/python

import time
import _inotify
import errno

def on_write(event):
    print('write')

def on_read(event):
    print("read")

def on_attrib(event):
    print("attribute change")

def on_move(event):
    print("move")

def on_open(event):
    print("open")

def on_close(event):
    print("close")

def on_delete_self(event):
    print("delete_self")

def on_create(event):
    print("create")

def on_delete(event):
    print("delete")

""" 
_inotify.MOVE = _inotify.MOVED_FROM | _inotify.MOVED_TO
_inotify.CLOSE = _inotify.CLOSE_WRITE | _inotify.CLOSE_NOWRITE

_inotify.MOVE, MOVED_FROM, MOVED_TO, DELETE
CREATE are  directory only masks
_inotify.ACCESS, MODIFY, OPEN, CLOSE,
CLOSE_WRITE, CLOSE_NOWRITE are file only masks.
"""

def response(event): 
    mask = event['mask']
    if mask & _inotify.ACCESS:
        on_read(event)
    elif mask & _inotify.MODIFY:
        on_write(event)
    elif mask & _inotify.ATTRIB:
        on_attrib(event)
    elif mask & _inotify.OPEN:
        on_open(event)
    elif mask & _inotify.CLOSE:
        on_close(event) 
    elif mask & _inotify.MOVE:
        on_move(event)
    elif mask & _inotify.DELETE_SELF:
        on_delete_self(event)
    elif mask & _inotify.DELETE:
        on_delete(event)
    elif mask & _inotify.CREATE:
        on_create(event)
    

fd = _inotify.create()
wd = _inotify.add(fd, "example", _inotify.ALL_EVENTS) 

while True:
    time.sleep(0.5)
    try:
        _inotify.read_event(fd, response)
    except OSError as e:
        if e.errno == errno.EAGAIN:
            pass


