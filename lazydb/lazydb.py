# -*- coding: utf-8 -*-
"""
    lazydb.py
    ~~~~~~~~~
    LazyDB is a basic wrapper around the Python shelve flatfile dbm
    module. LazyDB provides a couchdb/S3 like layer of abstraction around
    shelve, allowing convenient access (read and write) to shelve without
    sacrificing the convenience of writing pickled python objects to disk.

    :authors Mek
    :license GPLv3
"""

import os
import shelve
from contextlib import closing
from .utils import Storage

try:
    import pickle
except ImportError:
    import cPickle as pickle


class DBdefval(object):
    """Placeholder type for LazyDB default return value in the event a
    key is accessed when it doesn't exist (instead of raising an
    Exception)
    """
    pass


class Db(object):

    def __init__(self, path):
        """Creates a connection to a flatfile database located @ path
        using shelve wrappers. The database file will be
        created/touched during init, if no such file previously
        existed.
        """
        if '/' not in path:
            self._name = path
            self._file = "%s/%s" % (os.getcwd(), self._name)
        else:
            self._name = path.split('/')[-1]
            self._file = path
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
        """Crufty hack: Right now a new file handler is re-established
        every time a write is performed to ensure modifications to the
        shelve instance are saved / accepted."""
        self._db.close()
        self._db = self.open()

    def _destroy(self):
        return os.remove(self._file)

    def delete(self, key):
        if self.has(key):
            del self._db[key]
            return True

    def get(self, key, default=DBdefval, touch=False):
        """Retrieves all values within this LazyDB database indexed by
        this key. By default, an empty list is returned. Works similar
        to dict.get with default value if key doesn't exist.  Safely
        sets default as [] while carefully avoiding / preventing
        stateful decl of kwarg=[] within params list.
        """
        if default is DBdefval:
            default = []
        try:
            if not self.has(key) and touch:
                return self.put(key, default)
            return self._db.get(key, default)
        except (IndexError, KeyError, pickle.UnpicklingError):
            return default

    def put(self, key, record):
        """Adds a new key,val pair into the db. This will overwrite an
        existing key,val pair. To add an additonal entry to an
        existing record, use 'append'
        """
        self._db[key] = record
        self._write()  # XXX see _write docstring
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


def Orm(dbname, table):
    db = lambda: Db(dbname)

    class LazyOrm(Storage):

        def __init__(self, uuid=None, **data):
            if uuid:
                self._uuid = uuid
                data = data if data else self.get(uuid)
            try:
                for k, v in data.items():
                    setattr(self, k, v)
            except (AttributeError, IndexError) as e:
                raise e

        def __repr__(self):
            return '<LazyOrm ' + repr(dict(self)) + '>'

        def save(self):
            """save the state of the current item in the db; replace
            existing databased item (if it exists) with this dict() repr
            of this instance, or insert it otherwise
            """
            uuid = self.pop('_uuid', None)
            uuid = self.insert(dict(self), uuid=uuid)
            setattr(self, '_uuid', uuid)
            return uuid

        @classmethod
        def insert(cls, item, uuid=None):
            """
            """
            default = [] if uuid is None else {}
            vals = db().get(table, default=default, touch=True)

            if uuid and type(vals) is dict:
                vals.update({uuid: item})
            else:
                try:
                    vals.append(item)
                    uuid = len(vals)-1
                except AttributeError as e:
                    raise AttributeError('%s: Table %s.%s is of type dict and '
                                         "requires key 'uuid' for insertion."
                                         % (e, db._name, table))
            vals = db().put(table, vals)
            return uuid

        @classmethod
        def getall(cls, uuids=all, default=DBdefval):
            vals = db().get(table, default=default)
            if uuids is not all:
                if type(vals) is dict:
                    vals = dict(filter(lambda k, v: k in uuids, vals.items()))
                else:
                    vals = [v for i, v in enumerate(vals) if i in uuids]
            return vals

        @classmethod
        def get(cls, uuid, default=DBdefval):
            """
            """
            vals = cls.getall()
            try:
                return vals[uuid]
            except (KeyError, IndexError):
                return default

    return LazyOrm
