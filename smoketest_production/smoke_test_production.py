import erppeek
import unittest

class SmokeTestProduction(unittest.TestCase):

    SERVER = 'http://54.171.180.53'
    DATABASE = 'nhclinical'
    TEST_DATABASE = 'nhclinical_duplicate'
    USER = 'admin'
    PASSWORD = 'admin'

    @classmethod
    def setUpClass(cls):
        cls.client = erppeek.Client(server=cls.SERVER, db=cls.DATABASE, user=cls.USER, password=cls.PASSWORD)

        if cls.client.db.db_exist(cls.TEST_DATABASE):
            cls.client.db.drop(cls.USER, cls.TEST_DATABASE)

        cls.client.db.duplicate_database(cls.USER, cls.DATABASE, cls.TEST_DATABASE)

    def setUp(self):
        self.c = erppeek.Client(server=self.SERVER, db=self.TEST_DATABASE, user=self.USER, password=self.PASSWORD)

        self.p = self.c.model('nh.clinical.patient')
        self.a = self.client.model('nh.activity')
        self.s = self.client.model('nh.clinical.spell')
        self.l = self.client.model('nh.clinical.location')
        self.api = self.client.model('nh.eobs.api')

    @classmethod
    def tearDownClass(cls):
        cls.client.db.drop(cls.USER, cls.TEST_DATABASE)

    def test_port_8069_is_accessible(self):
        pass

    def test_port_5432_is_accessible(self):
        pass

    def test_example_patient_can_be_created(self):
        pass

    def test_example_ward_can_be_created(self):
        pass

    def test_example_user_can_be_created(self):
        pass

