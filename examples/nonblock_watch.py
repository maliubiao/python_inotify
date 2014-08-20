import _inotify
import select
import sys
import os
import fcntl
import errno
import pdb

def callback(event):
    print event

def do_poll(ep): 
    for fd, event in ep.poll(1): 
        while True:
            try:
                _inotify.read_event(fd, callback)
            except OSError as e:
                if e.errno == errno.EAGAIN:
                   break 
def main(): 
    fd = _inotify.create()
    wd = _inotify.add(fd, "cat", _inotify.ALL_EVENTS) 
    ep = select.epoll()
    ep.register(fd, select.EPOLLIN) 
    fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
    while True:
        try:
            do_poll(ep)
        except Exception as e:
            print e
            break 
    ep.close()
    os.close(fd)

if __name__ == "__main__":
    main() 

    
