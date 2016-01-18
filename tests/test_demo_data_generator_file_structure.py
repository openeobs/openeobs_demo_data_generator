from pyfakefs import fake_filesystem_unittest
import os
from demo_data_generators.demo_data_coordinator import DemoDataCoordinator
from demo_data_generators.admissions import AdmissionsGenerator
from demo_data_generators.locations import LocationsGenerator
from demo_data_generators.patients import PatientsGenerator
from demo_data_generators.placements import PlacementsGenerator
from demo_data_generators.pos import POSGenerator
from demo_data_generators.spells import SpellsGenerator
from demo_data_generators.users import UsersGenerator
from xml.etree.ElementTree import fromstring
from mock import MagicMock


class TestDemoDataGeneratorFileStructure(fake_filesystem_unittest.TestCase):

    def setUp(self):
        def fake_init(self, *args, **kwargs):
            self.root = fromstring('<openerp></openerp>')
            self.class_root = fromstring('<openerp></openerp>')
            self.data = fromstring('<data></data>')
            self.class_data = fromstring('<data></data>')
            self.users_schema = {
                'nurse': {
                    'total': 1,
                    'per_ward': 1,
                    'unassigned': 0,
                    'multi_wards': 0
                }
            }
            self.groups = {
                'hca': 'group_nhc_hca',
                'nurse': 'group_nhc_nurse',
                'ward_manager': 'group_nhc_ward_manager',
                'senior_manager': 'group_nhc_senior_manager',
                'doctor': 'group_nhc_doctor',
                'kiosk': 'group_nhc_kiosk',
                'admin': 'group_nhc_admin'
            }
            self.categories = {
                'hca': 'role_nhc_hca',
                'nurse': 'role_nhc_nurse',
                'ward_manager': 'role_nhc_ward_manager',
                'senior_manager': 'role_nhc_senior_manager',
                'doctor': 'role_nhc_doctor',
                'kiosk': 'role_nhc_kiosk',
                'admin': 'role_nhc_admin'
            }
            self.assignable_to_ward = (
                'ward_manager',
                'doctor',
                'kiosk',
            )
            self.assignable_to_bed = (
                'hca',
                'nurse',
            )

            self.names_generators = {
                'hca': (n for n in ['HCA']),
                'nurse': (n for n in ['NURSE', 'NURSE']),
                'ward_manager': (n for n in ['WARDMANAGER']),
                'senior_manager': (n for n in ['SENIORMANAGER']),
                'doctor': (n for n in ['DOCTOR']),
                'kiosk': (n for n in ['KIOSK']),
                'admin': (n for n in ['OLGA'])
            }
            self.timezone = 'Europe/London'
            self.data_generator = MagicMock()

        self.original_user_init = UsersGenerator.__init__
        self.original_spells_init = SpellsGenerator.__init__
        self.original_pos_init = POSGenerator.__init__
        self.original_placements_init = PlacementsGenerator.__init__
        self.original_patients_init = PatientsGenerator.__init__
        self.original_locations_init = LocationsGenerator.__init__
        self.original_admissions_init = AdmissionsGenerator.__init__

        UsersGenerator.__init__ = fake_init
        SpellsGenerator.__init__ = fake_init
        POSGenerator.__init__ = fake_init
        PlacementsGenerator.__init__ = fake_init
        PatientsGenerator.__init__ = fake_init
        LocationsGenerator.__init__ = fake_init
        AdmissionsGenerator.__init__ = fake_init

        self.setUpPyfakefs()
        self.assertFalse(os.path.isdir('/demo_data'))
        os.mkdir('/demo_data')
        self.assertTrue(os.path.isdir('/demo_data'))
        self.schema = {
            'nurse': {
                'total': 1,
                'per_ward': 1,
                'unassigned': 0,
                'multi_wards': 0
            }
        }

    def tearDown(self):
        UsersGenerator.__init__ = self.original_user_init
        SpellsGenerator.__init__ = self.original_spells_init
        POSGenerator.__init__ = self.original_pos_init
        PlacementsGenerator.__init__ = self.original_placements_init
        PatientsGenerator.__init__ = self.original_patients_init
        LocationsGenerator.__init__ = self.original_locations_init
        AdmissionsGenerator.__init__ = self.original_admissions_init

    def test_ward_files_are_saved_correctly(self):
        self.assertFalse(os.path.isdir('/demo_data/ward_a'))
        self.assertFalse(os.path.isdir('/demo_data/ward_b'))
        DemoDataCoordinator(['a', 'b'], 1, 1, 0, self.schema, '/demo_data')
        self.assertTrue(os.path.isdir('/demo_data/ward_a'))
        self.assertTrue(os.path.isdir('/demo_data/ward_b'))
        self.assertTrue(os.path.exists('/demo_data/pos.xml'))
        self.assertTrue(os.path.exists('/demo_data/users.xml'))
        self.assertTrue(os.path.exists('/demo_data/ward_a/demo_locations.xml'))
        self.assertTrue(os.path.exists('/demo_data/ward_b/demo_locations.xml'))
        self.assertTrue(os.path.exists('/demo_data/ward_a/demo_users.xml'))
        self.assertTrue(os.path.exists('/demo_data/ward_b/demo_users.xml'))
        self.assertTrue(os.path.exists('/demo_data/ward_a/demo_patients.xml'))
        self.assertTrue(os.path.exists('/demo_data/ward_b/demo_patients.xml'))
        self.assertTrue(os.path.exists('/demo_data/ward_a/demo_spells.xml'))
        self.assertTrue(os.path.exists('/demo_data/ward_b/demo_spells.xml'))
        self.assertTrue(
                os.path.exists('/demo_data/ward_a/demo_admissions.xml'))
        self.assertTrue(
                os.path.exists('/demo_data/ward_b/demo_admissions.xml'))
        self.assertTrue(
                os.path.exists('/demo_data/ward_a/demo_placements.xml'))
        self.assertTrue(
                os.path.exists('/demo_data/ward_b/demo_placements.xml'))