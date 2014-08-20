data1 = """\
_inotify.ACCESS: File was accessed (read).
_inotify.ATTRIB:  Metadata changed .
_inotify.CLOSE_WRITE:  File opened for writing was closed.
_inotify.CLOSE_NOWRITE:  File not opened for writing was closed.
_inotify.CREATE:  File/directory created in wached directory.
_inotify.DELETE:  File/directory deleted from watched directory.
_inotify.DELETE_SELF:  Watched file/directory was itself deleted.
_inotify.MODIFY:  File was modified.
_inotify.MOVE_SELF:  Watched file/directory was itself moved.
_inotify.MOVED_FROM:  File moved out of watched directory.
_inotify.MOVED_TO:  File moved into watched directory.
_inotify.OPEN:  File was opened.
_inotify.ALL_EVENTS: all above.
"""
data2 = """\
_inotify.Q_OVERFLOW:  Event queue overflowed.
_inotify.ISDIR:  Subject of this event is a directory.
_inotify.IGNORED:  Watch was removed explictly or automatically.
_inotify.UNMOUNT:  File system containing watched object was unmounted. _inotify.DONT_FOLLOW: Don't dereference path if it is a symbolic link.
_inotify.EXCL_UNLINK: Don't generate events for children after they have been unlinked from the watched directory.
_inotify.IN_MASK_ADD: Add (bitwise OR) events for this path if it already exists(instead of replacing mask).
_inotify.ONESHOT: Monitor path for one event, then remove from watch list.
_inotify.ONLYDIR: Only watch path if it is a directory.
"""

template = """
<table>
<thead>
<tr>
    <td> Flag </td>
    <td> Meaning </td>
</tr>
</thead>
<tbody>
%s
</tbody>
</table>
"""

def generate_table(data):
    lines = []
    for i in data.split("\n"): 
        d = i.split(":") 
        if len(d) < 2:
            continue 
        lines.append("<tr>\n<td>%s</td>\n<td>%s</td>\n</tr>\n" % (d[0], d[1]))
    return "".join(lines)
print "###Flags"
print template % generate_table(data1)
print "###Special Flags"
print template % generate_table(data2)
