#-*- coding: utf-8 -*-
"""
    lazydb.py
    ~~~~~~~~~
    
    Basic wrapper for shelve (flatfile diskstore)

    :authors Mek
    :license GPLv3
"""

import os
import shelve
from contextlib import closing

class Db(object):

    def __init__(self, database, dbpath=os.getcwd()):
        self.name = database
        self.file = "%s/%s" % (dbpath, database)
        self.db = self.connect()

    def connect(self):
        return shelve.open(self.file, 'c')

    def _destroy(self):
        try:
            return os.remove(self.file)
        except:
            return False

    def get(self, key):
        return self.db[key]

    def put(self, key, record):
        self.db[key] = record

    def show_keys(self):
        return self.db.keys()

    @classmethod
    def create(cls, create):
        with closing(shelve.open(DB, 'c')) as db:
            db.close()

    @classmethod
    def delete(self, database):
        try:
            return os.remove(self.file)
        except:
            return False        


