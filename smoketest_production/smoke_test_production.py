import erppeek
import unittest
import random
import string
import os
import pwd
from patient import DummyPatient


class ParametrizedTest(unittest.TestCase):

    def __init__(self, method_name='run_test', server=None, adminpw=None, adtpw=None):
        super(ParametrizedTest, self).__init__(method_name)
        self.admin_pw = adminpw
        self.adt_pw = adtpw
        self.server = server

    @staticmethod
    def parametrize(testcase_klass, server=None, adminpw=None, adtpw=None):
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in test_names:
            suite.addTest(testcase_klass(name, server=server, adminpw=adminpw, adtpw=adtpw))
        return suite


class ADT(ParametrizedTest):
    def test_adt_something(self):
        print "adt_pw=", self.adt_pw
        print "server=", self.server
        self.assertTrue(True)

