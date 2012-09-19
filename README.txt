======
LazyDB
======

LazyDB is a basic wrapper around the Python shelve flatfile dbm
module. LazyDB provides a couchdb/S3 like layer of abstraction around
shelve, allowing convenient access (read and write) to shelve without
sacrificing the convenience of writing pickled python objects to disk.

From the help(shelve) documentation: A "shelf" is a persistent,
dictionary-like object.  The difference with dbm databases is that the
values (not the keys!) in a shelf can be essentially arbitrary Python
objects -- anything that the "pickle" module can handle.  This
includes most class instances, recursive data types, and objects
containing lots of shared sub-objects.  The keys are ordinary strings.

Disclaimer: I wouldn't suggest using this module for production
projects as I predict it having difficulty scaling. LazyDB is ideal
for supporting smaller projects with light data in which the
programmer must move quickly and intends to implement an alternate db
solution sooner rather than later. The intent is to provide a more
elegant interface for utilizing the shelve module, not to create an
efficient replacement.

Typical usage often looks like this::

    #!/usr/bin/env Python
    
    from lazydb.lazydb import Db

    class LazyUser:
    	  def __init__(self, name):
	      self.name = name

    db = Db('mydb', '/home/user/')
    db.put('user', LazyUser('lazybones'))
    u = db.get('user')
    u.name

Contributors
============

Currently, this project is maintained by Mek.
