# coding=utf-8
import unittest

from demo_data_generators.placements import PlacementsGenerator
from demo_data_generators.patients import PatientsGenerator
from demo_data_generators.users import UsersGenerator
from demo_data_generators.ward_strategy import patients_factory, WardStrategy,\
    get_hca_nurse_users, get_role, Patient


class TestWardStrategy(unittest.TestCase):
    """
    Test that WardStrategy creates strategy.
    """

    def setUp(self):
        """
        WardStrategy needs patient placements.
        """
        bed_patient = PatientsGenerator(0, 2, 0, 'a')
        self.gen = PlacementsGenerator(bed_patient, [-1, -2])
        self.patients = patients_factory(self.gen.root)
        risk = {'high': 1, 'medium': 2, 'low': 10, 'none': 15}
        self.user_ids = ['user_1', 'user_2']
        self.strategy = WardStrategy(self.patients, self.user_ids, risk, 1)

    def test_pick_user_id(self):
        user_id = self.strategy.pick_user_id()

        self.assertTrue(user_id in self.user_ids)

    def test_get_hca_nurse_users(self):
        basic_schema = {
            'hca': {'total': 1, 'per_ward': 1, 'unassigned': 0},
            'nurse': {'total': 1, 'per_ward': 1, 'unassigned': 0}
        }
        gen = UsersGenerator(basic_schema)
        doc = gen.generate_users_per_ward('a', 2)

        user_ids = get_hca_nurse_users(doc)

        self.assertEqual(len(user_ids), 2)

    def test_get_role(self):
        hca = "[(4, ref('nh_clinical.role_nhc_hca'))]"
        basic_schema = {'hca': {'total': 1, 'per_ward': 1, 'unassigned': 0}}
        gen = UsersGenerator(basic_schema)
        doc = gen.generate_users_per_ward('a', 2)
        user = doc.findall(".//record/[@model='res.users']")[0]

        role = get_role(user)

        self.assertEqual(role, hca)


class TestPatient(unittest.TestCase):

    def setUp(self):
        """
        WardStrategy needs patient placements.
        """
        bed_patient = PatientsGenerator(0, 2, 0, 'a')
        self.gen = PlacementsGenerator(bed_patient, [-1, -2])

    def test_set_id(self):
        patient = Patient()
        patient.patient_id = "patient_12"

        patient.set_id()

        self.assertEqual(patient.id, '12')

    def test_patients_factory(self):
        patients = patients_factory(self.gen.root)
        patient_1 = patients[0]
        patient_2 = patients[1]

        self.assertEqual(len(patients), 2)

        self.assertEqual(patient_1.id, '0')
        self.assertEqual(patient_2.id, '1')

        self.assertEqual(patient_1.patient_id, 'nhc_demo_patient_0')
        self.assertEqual(patient_2.patient_id, 'nhc_demo_patient_1')

        self.assertEqual(patient_1.placement_id, 'nhc_demo_placement_0')
        self.assertEqual(patient_2.placement_id, 'nhc_demo_placement_1')

        self.assertEqual(patient_1.activity_id,
                         'nhc_activity_demo_placement_0')
        self.assertEqual(patient_2.activity_id,
                         'nhc_activity_demo_placement_1')

        self.assertEqual(patient_1.spell_activity_id,
                         'nhc_activity_demo_spell_0')
        self.assertEqual(patient_2.spell_activity_id,
                         'nhc_activity_demo_spell_1')





