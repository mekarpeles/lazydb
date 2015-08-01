import unittest
import uuid
import os
from lazydb.lazydb import Db, Orm


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
        db = Db(DB_PATH)  # NOQA
        self.assertTrue(os.path.exists(DB_PATH),
                        "Database creation failed.")

    def test_orm_dict(self):
        Item = Orm(DB_PATH, TEST_KEY)
        i = Item(TEST_KEY, **TEST_ITEM)
        i.save()
        items = i.getall()
        self.assertTrue(TEST_KEY in items[TEST_KEY] and
                        items[TEST_KEY][TEST_KEY].name == TEST_VAL.name,
                        "Item not added correctly to dict style ORM: "
                        "%s" % items)

    def test_orm_list(self):
        Item = Orm(DB_PATH, TEST_KEY)
        i = Item(**TEST_ITEM)
        i.save()
        items = i.getall()
        self.assertTrue(TEST_KEY in items[0] and
                        items[0][TEST_KEY].name == TEST_VAL.name,
                        "Item not added correctly to list style ORM: "
                        "%s" % items)

    def test_put(self):
        db = Db(DB_PATH)
        db.put(TEST_KEY, TEST_VAL)
        db_val = db.get(TEST_KEY)
        print("PUT: %s, GET: %s" % (TEST_ITEM, db_val))
        self.assertTrue(db_val.__dict__ == TEST_VAL.__dict__,
                        "Failed to 'put' TEST_ITEM %s "
                        "into %s" % (TEST_ITEM, DB_NAME))

    def test_get_keyerror(self):
        """Tests a db.get(key) on a key which doesn't exist"""
        db = Db(DB_PATH)
        v = None
        try:
            v = db.get(TEST_KEY + "KEYERROR", default={}, touch=False)
        except KeyError:
            self.assertTrue(v is None, "db.get() touched/create a table "
                            "and it shouldn't have (because touch=False).")
        v = db.get(TEST_KEY + "KEYERROR", default={}, touch=True)
        self.assertTrue(v == {}, "db.get() was supposed to touched/create "
                        "a table but it didn't (because touch=True).")

    def test_append(self):
        db = Db(DB_PATH)
        db.put(TEST_KEY, TEST_VAL)
        db.append(TEST_KEY, TEST_VAL)
        db_val = db.get(TEST_KEY)
        print("APPEND: %s, GET: %s" % (TEST_ITEM, db_val))
        self.assertTrue(map(lambda x: x.__class__, db_val) ==
                        map(lambda x: x.__class__, [TEST_VAL] * 2),
                        "Failed to 'append' TEST_ITEM %s "
                        "into %s" % (TEST_ITEM, DB_NAME))

    def tearDown(self):
        db = Db(DB_PATH)
        db._destroy()
        self.assertTrue(not os.path.exists(DB_PATH),
                        "Database failed to destroy tmp db %s" % DB_PATH)
