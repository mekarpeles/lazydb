import unittest
import uuid
import os
from lazydb.lazydb import Db

class LazyUser:
    def __init__(self, name):
        self.name = name    

DB_NAME = uuid.uuid1()
DB_PATH = "%s/test/%s" % (os.getcwd(), DB_NAME)
TEST_KEY = "user"
TEST_VAL = LazyUser('lazybones')
TEST_ITEM = {TEST_KEY: TEST_VAL}

class TestLazyDB(unittest.TestCase):

    def setUp(self):
        db = Db(DB_PATH)
        self.assertTrue(os.path.exists(DB_PATH),
                        "Database creation failed.")
        
    def test_put(self):
        db = Db(DB_PATH)
        db.put(TEST_KEY, TEST_VAL)
        db_val = db.get(TEST_KEY)
        print "PUT: %s, GET: %s" % (TEST_ITEM, db_val)
        self.assertTrue(db_val.__dict__ == TEST_VAL.__dict__,
                        "Failed to 'put' TEST_ITEM %s " \
                            "into %s" % (TEST_ITEM, DB_NAME))

    def test_append(self):
        db = Db(DB_PATH)
        db.put(TEST_KEY, TEST_VAL)
        db.append(TEST_KEY, TEST_VAL)
        db_val = db.get(TEST_KEY)
        print "APPEND: %s, GET: %s" % (TEST_ITEM, db_val)
        self.assertTrue(map(lambda x: x.__class__, db_val) == \
                            map(lambda x: x.__class__, [TEST_VAL] * 2),
                        "Failed to 'append' TEST_ITEM %s " \
                            "into %s" % (TEST_ITEM, DB_NAME))

    def test_props(self):
        db = Db(DB_PATH)
        NotImplemented

    def tearDown(self):
        db = Db(DB_PATH)
        db._destroy()
        self.assertTrue(not os.path.exists(DB_PATH),
                        "Database failed to destroy tmp db %s" % DB_PATH)
