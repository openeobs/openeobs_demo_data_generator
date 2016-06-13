import erppeek
import unittest
import random
import string
import os
import pwd
from patient import DummyPatient


class ParametrizedTest(unittest.TestCase):

    def __init__(self, method_name='run_test', server=None):
        super(ParametrizedTest, self).__init__(method_name)
        self.server = server

    @classmethod
    def setUpClass(cls):
        cls.ep_client = erppeek.Client(server=server.server, db=db, user='admin', password='lrrfhkbkgthrbidjlhdrhtckcckbtetj')

    @staticmethod
    def parametrize(testcase_klass, server=None):
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in test_names:
            suite.addTest(testcase_klass(name, server=server))
        return suite


class ADT(ParametrizedTest):
    def test_adt_register_patient(self):
        print self.server
        #result = self.api.register(self.patient.hospitalnumber, self.patient.__dict__)
        #self.assertTrue(result, "Patient was not registered")

    #def test_adt_admit_patient(self):
    #    self.patient.location = 'A1'
    #    self.patient.start_date = '01-06-2016'
    #    result = self.admit_patient()
    #    self.assertTrue(result, "Patient was not admitted")

