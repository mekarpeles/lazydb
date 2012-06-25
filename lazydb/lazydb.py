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
        self._name = database
        self._file = "%s/%s" % (dbpath, database)
        self._db = self.connect()

    def connect(self):
        return shelve.open(self._file, 'c')

    def _write(self):
        self._db.close()
        self._db = self.connect()
        
    def _destroy(self):
        return os.remove(self._file)

    def delete(self, key):
        if self.has(key):
            del self._db[key]
            return True

    def get(self, key):
        return self._db.get(key, [])

    def put(self, key, record):
        self._db[key] = record
        self._write()
        return record

    def has(self, key):        
        return key in self._db.keys()

    def empty(self):
        """boolean check to see if the database has any keys"""
        return self.count()
            
    @property
    def count(self):
        """Counts the number of keys"""        
        return len(self._db.keys())

    @property
    def keys(self):
        """List keys in the db"""
        return self._db.keys()

    def records(self, key):
        """length of the contents of a record"""
        return len(self._db.get(key, []))

    def append(self, key, record):
        """should only work if obj @ key is type([])"""
        records = self.get(key) + [record]
        self.put(key, records)
        self._write()

    @classmethod
    def create(cls, create):
        with closing(shelve.open(DB, 'c')) as db:
            db.close()

    @classmethod
    def destroy(self, database):
        return os.remove(self._file)
