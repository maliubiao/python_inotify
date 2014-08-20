if __name__ == "__main__":
    import _inotify 
    import sys
    import time
    import pdb
    import errno
    if len(sys.argv) < 2:
        print("require a file.")
        exit()

    target = sys.argv[1]
    consts = {
            _inotify.ACCESS: "File was accessed (read)",
            _inotify.ATTRIB: "Metadata changed ",
            _inotify.CLOSE_WRITE: "File opened for writing was closed",
            _inotify.CLOSE_NOWRITE: "File not opened for writing was closed",  
            _inotify.CREATE: "File/directory created in wached directory",
            _inotify.DELETE: "File/directory deleted from watched directory",
            _inotify.DELETE_SELF: "Watched file/directory was itself deleted",
            _inotify.MODIFY: "File was modified",
            _inotify.MOVE_SELF: "Watched file/directory was itself moved",
            _inotify.MOVED_FROM: "File moved out of watched directory",
            _inotify.MOVED_TO: "File moved into watched directory",
            _inotify.OPEN: "File was opened",
            _inotify.IGNORED: "Watch was removed explictily",
            _inotify.ISDIR: "Subject of this event is a directory",
            _inotify.Q_OVERFLOW: "Event queue overflowed",
            _inotify.UNMOUNT: "File system containing watched object was unmounted",
            _inotify.IGNORED: "Watch was removed explictly or automatically",
            _inotify.ISDIR: "Subject of this event is a directory",
            _inotify.Q_OVERFLOW: "Event queue overflowed",
            _inotify.UNMOUNT: "File system containing watched object was unmounted"
    } 
            
    def callback(event): 
        mask = event["mask"]
        for k, v in consts.items():
            if mask & k: 
                print("%s: %s" % (target, v)) 

    fd = _inotify.create()
    wd = _inotify.add(fd, target, _inotify.ALL_EVENTS)
    while True:
        time.sleep(0.1)
        try:
            _inotify.read_event(fd, callback) 
        except OSError as e:
            if e.errno == errno.EAGAIN:
                pass
        
