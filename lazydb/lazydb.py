#-*- coding: utf-8 -*-
"""
    lazydb.py
    ~~~~~~~~~
    LazyDB is a basic wrapper around the Python shelve flatfilqe dbm
    module. LazyDB provides a couchdb/S3 like layer of abstraction around
    shelve, allowing convenient access (read and write) to shelve without
    sacrificing the convenience of writing pickled python objects to disk.

    :authors Mek
    :license GPLv3
"""

import os
import shelve
from contextlib import closing

class Db(object):

    def __init__(self, db_name, db_path=os.getcwd()):
        """Creates a connection to a flatfile database located in
        db_path and named db_path using shelve wrappers. The database
        file will be created/touched during init, if no such file
        previously existed.
        """
        self._name = db_name
        self._file = "{}/{}".format(db_path, db_name)
        self._db = self.open()

    def open(self):
        return shelve.open(self._file, 'c')

    def close(self):
        return self._db.close()

    @property
    def connected(self):
        """Test whether a connection is open"""
        pass

    @property
    def dict(self):
        return dict(self.items())

    def _write(self):
        """Crufty hack"""
        self._db.close()
        self._db = self.open()
        
    def _destroy(self):
        return os.remove(self._file)

    def delete(self, key):
        if self.has(key):
            del self._db[key]
            return True

    def get(self, key):
        return self._db.get(key, [])

    def put(self, key, record):
        """Adds a new key,val pair into the db. This will overwrite an
        existing key,val pair. To add an additonal entry to an
        existing record, use 'append'
        """
        self._db[key] = record
        self._write() # XXX see _write docstring
        return self.get(key)

    def has(self, key):        
        """Determines whether a key exists within the database"""        
        return key in self.keys()

    def count(self, key):
        """Returns the number of entries within a record"""
        return len(self._db.get(key, []))

    def is_empty(self):
        """boolean check to see if the database has any keys. Returns
        0 if empty, else the number of keys in the db
        """
        return self.size()

    def size(self):
        """Returns the size of the database in number of entries"""
        return len(self.keys())
    
    def keys(self):
        """List keys in the db"""
        return self._db.keys()

    def values(self):
        """List all the values in the db"""
        return [self.get(key) for key in self.keys()]

    def items(self):
        return [(key, self.get(key)) for key in self.keys()]

    def append(self, key, record):
        """should only work if obj @ key is type([])"""
        records = self.get(key)
        if not type(records) is list:
            records = [records]        
        records = self.put(key, records + [record])
        self._write()
        return records

    def update(self, key, index, record):
        """Update a specific value entry/record specified by index
        keyed by key. The index, i.e. the position of the entry to
        update, is 0 indexed.
        """
        values = self.get(key)
        values[index] = record
        return self.put(key, values)

    @classmethod
    def create(cls, database):
        """Used for creating arbitrary tmp databases"""
        with closing(shelve.open(database, 'c')) as db:
            db.close()

    @classmethod
    def destroy(self, database):
        """Used for cleanup of arbitrary tmp databases"""
        return os.remove(database)
