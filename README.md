python-inotify
==============
python binding for linux inotify 

* License     :MIT 

## Demo 
```python
#! /usr/bin/env python

"""
backup your file automatically.  
"""

import os
import time
import shutil
import sys
import errno 
import os.path
try:
    import _inotify
except:
    print "install _inotify please, url:  https://github.com/maliubiao/python_inotify"
    exit(0)


backup_dst = "/dropbox/path/backup"

backup_list = [
        "/home/user/.vimrc",
        "/home/user/.bashrc"
        ] 


#ident -> file
wds = {}

#inotify fd
fd = 0

#log
log_path = "/tmp/backup.log"

#touch down wd
twd = 0

#touch down path
tpath = "/tmp/backup.down"

def recv(event): 
    mask = event["mask"] 
    wd = event["wd"]            
    f = wds[wd] 
    if (mask & _inotify.MODIFY) or (mask & _inotify.CLOSE_WRITE) or (mask & _inotify.ATTRIB): 
        if wd == twd:
            print "yes, exit....."
            exit(0) 
        print "backup:", time.ctime(), f 
        try:
            shutil.copyfile(f,  backup_dst + os.path.basename(f))
        except OSError as e:
            print e 
    if mask & _inotify.DELETE_SELF:
        print f, " was itself deleted, add it again"
        try:
            wd2 = _inotify.add(fd, f, _inotify.ALL_EVENTS) 
            wds[wd2] = f 
        except OSError as e:
            print e 
    if mask & _inotify.IGNORED:
        del wds[wd]


def touch_down():
    global twd 
    f = open(tpath, "w+")
    f.close()
    try:
        twd = _inotify.add(fd, tpath, _inotify.ALL_EVENTS)
        wds[twd] = tpath
    except OSError:
        print i, e


def backup(*args):
    global fd
    fd = _inotify.create() 
    for i in backup_list: 
        try:
            wd = _inotify.add(fd, i, _inotify.ALL_EVENTS)
            wds[wd] = i 
        except OSError as e:
            print i, e
    touch_down()
    while True:
        time.sleep(0.5)
        try:
            _inotify.read_event(fd, recv)
        except OSError as e: 
            if e.errno == errno.EAGAIN:
                pass 


def background_backup(*args): 
    if os.fork() == 0:
        os.setsid()        
        sys.stdin = open('/dev/null', "r")
        output = open(log_path, "w+", buffering=0)
        sys.stdout = output
        sys.stderr = output
        if os.fork() == 0:
            backup(*args)
        else:
            exit(0)
    else:
        exit(0)

if __name__ == "__main__": 
    backup()

```

## Examples
    
    see examples/ 

## API
####inotify_fd = _inotify.create()
initializes a new inotify instance and returns a file descriptor associated with a new inotify event queue. You can use os.close(inotify_fd) to close this fd;

####wd = _inotify.add(inotify_fd, path, flags)
adds a new watch, or modifies an existing watch, for the file whose locaion is specified in pathname.
###Flags

####_inotify.remove(inotify_fd, wd)
removes the watch associated with the watch descriptor wd from the inotify instance associated with the file descriptor fd. Removing a watch causes an IGNORED event.

####_inotify.read_event(inotify_fd, callback)
raise IOError with errno = EAGAIN if there is no event in the queue, otherwise invoke callback with a dict: {wd, mask, cookie, name, len}, see examples/;

<table>
<thead>
<tr>
    <td> Flag </td>
    <td> Meaning </td>
</tr>
</thead>
<tbody>
<tr>
<td>_inotify.ACCESS</td>
<td> File was accessed (read).</td>
</tr>
<tr>
<td>_inotify.ATTRIB</td>
<td>  Metadata changed .</td>
</tr>
<tr>
<td>_inotify.CLOSE_WRITE</td>
<td>  File opened for writing was closed.</td>
</tr>
<tr>
<td>_inotify.CLOSE_NOWRITE</td>
<td>  File not opened for writing was closed.</td>
</tr>
<tr>
<td>_inotify.CREATE</td>
<td>  File/directory created in wached directory.</td>
</tr>
<tr>
<td>_inotify.DELETE</td>
<td>  File/directory deleted from watched directory.</td>
</tr>
<tr>
<td>_inotify.DELETE_SELF</td>
<td>  Watched file/directory was itself deleted.</td>
</tr>
<tr>
<td>_inotify.MODIFY</td>
<td>  File was modified.</td>
</tr>
<tr>
<td>_inotify.MOVE_SELF</td>
<td>  Watched file/directory was itself moved.</td>
</tr>
<tr>
<td>_inotify.MOVED_FROM</td>
<td>  File moved out of watched directory.</td>
</tr>
<tr>
<td>_inotify.MOVED_TO</td>
<td>  File moved into watched directory.</td>
</tr>
<tr>
<td>_inotify.OPEN</td>
<td>  File was opened.</td>
</tr>
<tr>
<td>_inotify.ALL_EVENTS</td>
<td> all above.</td>
</tr>

</tbody>
</table>

###Special Flags

<table>
<thead>
<tr>
    <td> Flag </td>
    <td> Meaning </td>
</tr>
</thead>
<tbody>
<tr>
<td>_inotify.Q_OVERFLOW</td>
<td>  Event queue overflowed.</td>
</tr>
<tr>
<td>_inotify.ISDIR</td>
<td>  Subject of this event is a directory.</td>
</tr>
<tr>
<td>_inotify.IGNORED</td>
<td>  Watch was removed explictly or automatically.</td>
</tr>
<tr>
<td>_inotify.UNMOUNT</td>
<td>  File system containing watched object was unmounted. _inotify.DONT_FOLLOW</td>
</tr>
<tr>
<td>_inotify.EXCL_UNLINK</td>
<td> Don't generate events for children after they have been unlinked from the watched directory.</td>
</tr>
<tr>
<td>_inotify.IN_MASK_ADD</td>
<td> Add (bitwise OR) events for this path if it already exists(instead of replacing mask).</td>
</tr>
<tr>
<td>_inotify.ONESHOT</td>
<td> Monitor path for one event, then remove from watch list.</td>
</tr>
<tr>
<td>_inotify.ONLYDIR</td>
<td> Only watch path if it is a directory.</td>
</tr>

</tbody>
</table>


###
## Install 
    #git clone https://github.com/maliubiao/python-inotify.git
    #cd python-inotify
    #sudo python setup.py install

