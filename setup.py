#! /usr/bin/env python
from distutils.core import setup, Extension

m = Extension('_inotify',
        sources = ['inotify.c'] 
        )


setup(name = 'inotify',
        version = '1.0',
        description = 'python binding for linux inotify.',
        ext_modules = [m])
