import erppeek
import unittest
import random
import string
import os
#from pwd import getpwuid
import pwd
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
        self.u = self.c.model('res.users')
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

    def test_create_location(self):
        result = self.l.create({'usage': 'bed', 'type': 'pos', 'name': 'SmokeTest bed'})
        self.assertTrue(result.id > 0)

    def test_create_user(self):
        result = self.u.create({'name': 'Nurse 1', 'login': 'nurse_01', 'password': 'user_000'})
        self.assertTrue(result.id > 0)

    def test_module_nh_eobs_adt_gui_is_installed(self):
        modules = self.c.modules(installed=True)
        self.assertIn('nh_eobs_adt_gui', modules.get('installed'))

    def test_module_nh_eobs_slam_is_installed(self):
        modules = self.c.modules(installed=True)
        self.assertIn('nh_eobs_slam', modules.get('installed'))

    def test_module_nh_eobs_backup_is_installed(self):
        modules = self.c.modules(installed=True)
        self.assertIn('nh_eobs_backup', modules.get('installed'))

    def test_log_files_exist_and_are_not_empty(self):
        log_file = "/var/log/odoo/odoo_server.log"
        self.assertTrue(os.path.exists(log_file), log_file + " doesn't exist")

        self.assertTrue(os.path.getsize(log_file) > 0, log_file + " is empty")

    def test_bcp_directory_exists_and_has_right_permissions(self):
        backup_path = "/bcp"
        self.assertTrue(os.path.exists(backup_path), backup_path + " doesn't exist")
        self.assertTrue(pwd.getpwuid(os.stat(backup_path).st_uid).pw_name == "odoo", backup_path + " owner is not 'odoo'")

    def test_odoo_backup_cronjob_is_present(self):
        model = self.c.model('ir.cron')
        record = model.browse([])
        cronjob_list = model.read(record._idnames)

        self.assertTrue((d['function'] == 'print_report' for d in cronjob_list), "print_report cronjob not installed")

    def admit_patient(self):
        return self.api.admit(self.patient.hospitalnumber, self.patient.__dict__)
