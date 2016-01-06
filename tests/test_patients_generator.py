from demo_data_generators.patients import PatientsGenerator
import unittest


class TestPatientsGenerator(unittest.TestCase):
    """
    Test that the patients generator does indeed generate patients
    """

    def test_01_has_ethnicity_list(self):
        """
        PatientGenerator has an ethnicity list property, make sure it def does
        """
        patientgen = PatientsGenerator(0, 0, 0, 'a')
        ethnicity_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J',
                               'K', 'L', 'M', 'N', 'P', 'R', 'S', 'Z']
        self.assertEqual(ethnicity_list, patientgen.ethnicity_list,
                         'Ethnicity list incorrect')
