# coding=utf-8
import unittest

from demo_data_generators.placements import PlacementsGenerator
from demo_data_generators.patients import PatientsGenerator
from demo_data_generators.ward_strategy import patients_factory, WardStrategy


class TestWardStrategy(unittest.TestCase):
    """
    Test that WardStrategy creates strategy.
    """

    def setUp(self):
        """
        WardStrategy needs patient placements.
        """
        bed_patient = PatientsGenerator(0, 2, 0, 'a')
        self.gen = PlacementsGenerator(bed_patient)

    def test_patients_factory(self):
        patients = patients_factory(self.gen.root)
        self.assertEqual(len(patients), 2)

        patient_1 = patients[0]
        patient_2 = patients[1]
        self.assertEqual(patient_1.id, '0')
        self.assertEqual(patient_2.id, '1')

    def test_ward_strategy(self):
        patients = patients_factory(self.gen.root)
        risk_distribution = {'high': 1, 'medium': 2, 'low': 10, 'none': 15}
        ward_strategy = WardStrategy(patients, risk_distribution, 1)

        self.assertEqual(len(ward_strategy.patients), 2)
        self.assertEqual(ward_strategy.partial_news_per_patient, 1)






