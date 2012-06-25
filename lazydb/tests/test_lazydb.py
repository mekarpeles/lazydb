import unittest
import uuid
import os
from lazydb.lazydb import Db

DBNAME = uuid.uuid1()

class TestLazyDB(unittest.TestCase):

    def test_creation(self):
        db = Db(DBNAME)
        self.assertTrue(os.path.exists("%s/tests/%s" % (os.getcwd(), DBNAME)))
        

        
        
