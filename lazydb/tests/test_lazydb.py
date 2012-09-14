import unittest
import uuid
import os
from lazydb.lazydb import Db

DB_NAME = uuid.uuid1()
DB_PATH = "{}/tests/".format(os.getcwd())

class TestLazyDB(unittest.TestCase):

    def setUp(self):
        db = Db(db_name=DB_NAME, db_path=DB_PATH)
        self.assertTrue(os.path.exists("{}{}".format(DB_PATH, DB_NAME)),
                        "Database creation failed.")
        
    def tearDown(self):
        db = Db(db_name=DB_NAME, db_path=DB_PATH)
        db._destroy()
        self.assertTrue(os.path.exists("{}{}".format(DB_PATH, DB_NAME)),
                        "Database deletion failed.")
        
        
