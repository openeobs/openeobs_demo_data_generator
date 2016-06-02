import erppeek
import unittest
import random
import string
import os
from patient import DummyPatient


class SmokeTestProduction(unittest.TestCase):

    SERVER = os.environ['SERVER']
    DATABASE = 'nhclinical'
    TEST_DATABASE = 'nhclinical_duplicate'
    ADMIN_USER = 'admin'
    ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
    ADT_USER = 'adt'
    ADT_PASSWORD = os.environ['ADT_PASSWORD']

    @classmethod
    def setUpClass(cls):
        cls.client = erppeek.Client(server=cls.SERVER, db=cls.DATABASE, user=cls.ADMIN_USER, password=cls.ADMIN_PASSWORD)

        if cls.client.db.db_exist(cls.TEST_DATABASE):
            cls.client.db.drop(cls.ADMIN_USER, cls.TEST_DATABASE)

        cls.client.db.duplicate_database(cls.ADMIN_USER, cls.DATABASE, cls.TEST_DATABASE)

    def setUp(self):
        self.c = erppeek.Client(server=self.SERVER, db=self.TEST_DATABASE, user=self.ADT_USER, password=self.ADT_PASSWORD)

        self.p = self.c.model('nh.clinical.patient')
        self.a = self.c.model('nh.activity')
        self.s = self.c.model('nh.clinical.spell')
        self.l = self.c.model('nh.clinical.location')
        self.api = self.c.model('nh.eobs.api')

        # Set up a new patient for each test
        hospnumber = ''.join(random.sample(string.digits*6, 6))
        charset = string.ascii_uppercase + string.digits
        nhsnumber = ''.join(random.sample(charset*8, 8))
        self.patient = DummyPatient(hospitalnumber=hospnumber, patient_identifier=nhsnumber, family_name="Meyers",
                                    given_name="Mike", sex='M', dob='10-10-1950')

    @classmethod
    def tearDownClass(cls):
        pass
        cls.client.db.drop(cls.ADMIN_USER, cls.TEST_DATABASE)

    def test_port_8069_is_accessible(self):
        pass

    def test_port_5432_is_accessible(self):
        pass

    def test_register_patient(self):
        result = self.api.register(self.patient.hospitalnumber, self.patient.__dict__)
        self.assertTrue(result, "Patient was not registered")

    def test_admit_patient(self):
        self.patient.location = 'A1'
        self.patient.start_date = '01-06-2016'
        result = self.admit_patient(self.patient, self.api)
        self.assertTrue(result, "Patient was not admitted")

    def test_transfer_patient(self):
        self.patient.location = 'A2'
        self.patient.start_date = '01-06-2016'
        self.admit_patient(self.patient, self.api)

        self.patient.location = 'A22'
        result = self.api.transfer(self.patient.hospitalnumber, self.patient.__dict__)
        self.assertTrue(result, "Patient was not transferred")

    def test_discharge_patient(self):
        self.patient.location = 'A3'
        self.patient.start_date = '01-06-2016'
        self.admit_patient(self.patient, self.api)

        self.patient.POS = 'NW12'
        result = self.api.discharge(self.patient.hospitalnumber, self.patient.__dict__)
        self.assertTrue(result, "Patient wasn't discharged")

    def admit_patient(self, patient, api):
        return api.admit(patient.hospitalnumber, patient.__dict__)

    #def test_nhs_number_needed(self):
        #self.patient.patient_identifier = ""
    #    self.assertFalse(self.api.register(self.patient.hospitalnumber, self.patient.__dict__),
    #                     "Patient was registered without NHS number")
