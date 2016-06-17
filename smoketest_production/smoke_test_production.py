import erppeek
import unittest
import random
import string
import os
import pwd
from patient import DummyPatient


class ParametrizedTest(unittest.TestCase):

    def __init__(self, method_name='run_test', client=None):
        super(ParametrizedTest, self).__init__(method_name)
        self.client = client

        self.p = self.client.model('nh.clinical.patient')
        self.a = self.client.model('nh.activity')
        self.s = self.client.model('nh.clinical.spell')
        self.l = self.client.model('nh.clinical.location')
        self.u = self.client.model('res.users')
        self.api = self.client.model('nh.eobs.api')

        # Set up a new patient for each test
        hospnumber = ''.join(random.sample(string.digits * 6, 6))
        charset = string.ascii_uppercase + string.digits
        nhsnumber = ''.join(random.sample(charset * 8, 8))
        self.patient = DummyPatient(hospitalnumber=hospnumber, patient_identifier=nhsnumber, family_name="Meyers",
                                    given_name="Mike", sex='M', dob='10-10-1950')

    @staticmethod
    def parametrize(testcase_klass, client=None):
        test_loader = unittest.TestLoader()
        test_names = test_loader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in test_names:
            suite.addTest(testcase_klass(name, client=client))
        return suite


class ADT(ParametrizedTest):

    def test_adt_register_patient(self):
        result = self.api.register(self.patient.hospitalnumber, self.patient.__dict__)
        self.assertTrue(result, "Patient was not registered")

    def test_adt_admit_patient(self):
        self.patient.location = 'A1'
        self.patient.start_date = '01-06-2016'
        result = self.admit_patient()
        self.assertTrue(result, "Patient was not admitted")

    def test_adt_transfer_patient(self):
        self.patient.location = 'A2'
        self.patient.start_date = '01-06-2016'
        self.assertTrue(self.admit_patient())

        self.patient.location = 'A22'
        result = self.api.transfer(self.patient.hospitalnumber, self.patient.__dict__)
        self.assertTrue(result, "Patient was not transferred")

    def test_adt_discharge_patient(self):
        self.patient.location = 'A3'
        self.patient.start_date = '01-06-2016'
        self.assertTrue(self.admit_patient())

        self.patient.POS = 'NW12'
        result = self.api.discharge(self.patient.hospitalnumber, self.patient.__dict__)
        self.assertTrue(result, "Patient wasn't discharged")

    def admit_patient(self):
        return self.api.admit(self.patient.hospitalnumber, self.patient.__dict__)


class EObsUser(ParametrizedTest):
    def test_create_location(self):
        result = self.l.create({'usage': 'bed', 'type': 'pos', 'name': 'SmokeTest bed'})
        self.assertTrue(result.id > 0)

    def test_create_user(self):
        result = self.u.create({'name': 'Nurse 1', 'login': 'nurse_01', 'password': 'user_000'})
        self.assertTrue(result.id > 0)


class Modules(ParametrizedTest):
    def test_module_nh_eobs_adt_gui_is_installed(self):
        modules = self.client.modules(installed=True)
        self.assertIn('nh_eobs_adt_gui', modules.get('installed'))

    def test_module_nh_eobs_slam_is_installed(self):
        modules = self.client.modules(installed=True)
        self.assertIn('nh_eobs_slam', modules.get('installed'))

    def test_module_nh_eobs_backup_is_installed(self):
        modules = self.client.modules(installed=True)
        self.assertIn('nh_eobs_backup', modules.get('installed'))


class BackupModule(ParametrizedTest):
    def test_log_files_exist_and_are_not_empty(self):
        log_file = "/var/log/odoo/odoo_server.log"
        self.assertTrue(os.path.exists(log_file), log_file + " doesn't exist")

        self.assertTrue(os.path.getsize(log_file) > 0, log_file + " is empty")

    def test_bcp_directory_exists_and_has_right_permissions(self):
        backup_path = "/bcp"
        self.assertTrue(os.path.exists(backup_path), backup_path + " doesn't exist")
        self.assertTrue(pwd.getpwuid(os.stat(backup_path).st_uid).pw_name == "odoo",
                        backup_path + " owner is not 'odoo'")

    def test_odoo_backup_cronjob_is_present(self):
        model = self.client.model('ir.cron')
        record = model.browse([])
        cronjob_list = model.read(record._idnames)

        self.assertTrue((d['function'] == 'print_report' for d in cronjob_list), "print_report cronjob not installed")
