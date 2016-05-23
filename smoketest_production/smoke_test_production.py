import erppeek
import unittest

class SmokeTestProduction(unittest.TestCase):

    SERVER = 'http://localhost:8069'
    DATABASE = 'nhclinical'
    TEST_DATABASE = 'nhclinical_duplicate'
    USER = 'admin'
    PASSWORD = 'admin'

    def setUp(self):
        self.client = erppeek.Client(server=self.SERVER, db=self.DATABASE, user=self.USER, password=self.PASSWORD)

        self.client.db.duplicate_database(self.USER, self.DATABASE, self.TEST_DATABASE)

        self.client = self.client.login(self.USER, self.PASSWORD, self.TEST_DATABASE)

        self.p = self.client.model('nh.clinical.patient')
        self.a = self.client.model('nh.activity')
        self.s = self.client.model('nh.clinical.spell')
        self.l = self.client.model('nh.clinical.location')
        self.api = self.client.model('nh.eobs.api')

    def test_patient_can_be_created(self):

    def test_ward_can_be_created(self):

    def test_user_can_be_created(self):

