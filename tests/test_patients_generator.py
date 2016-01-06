import unittest
from demo_data_generators.patients import PatientsGenerator


class TestPatientsGenerator(unittest.TestCase):
    """
    Test that the patients generator does indeed generate patients
    """

    def test_has_ethnicity_list(self):
        """
        PatientGenerator has an ethnicity list property, make sure it def does
        """
        patientgen = PatientsGenerator(0, 0, 0, 'a')
        ethnicity_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J',
                               'K', 'L', 'M', 'N', 'P', 'R', 'S', 'Z']
        self.assertEqual(ethnicity_list, patientgen.ethnicity_list,
                         'Ethnicity list incorrect')

    def test_no_update_on_data_element(self):
        """
        Make sure that the data element in the output has the noupdate flag
        set to True
        """
        patientgen = PatientsGenerator(0, 0, 0, 'a')
        no_update = patientgen.data.attrib['noupdate']
        self.assertEqual(no_update, '1', 'Incorrect noupdate flag')

    def test_has_gender_list(self):
        """
        Make sure that the PatientGenerator class has a gender list
        """
        patientgen = PatientsGenerator(0, 0, 0, 'a')
        gender_list = ['M', 'F']
        self.assertEqual(gender_list, patientgen.gender_sex_list,
                         'Incorrect Gender Sex List')

    def test_creates_number_of_defined_in_bed_records(self):
        """
        Make sure that it generates the number of defined records for patients
        in bed
        """
        patientgen = PatientsGenerator(0, 4, 0, 'a')
        records = patientgen.data.findall('record')
        self.assertEqual(4, len(records),
                         'Incorrect number of records generated')

    def test_creates_number_of_defined_not_in_bed_records(self):
        """
        Make sure that it generates the number of defined records for patients
        not in bed
        """
        patientgen = PatientsGenerator(0, 0, 4, 'a')
        records = patientgen.data.findall('record')
        self.assertEqual(4, len(records),
                         'Incorrect number of records generated')

    def test_creates_number_of_defined_records(self):
        """
        Make sure that it generates the number of defined records for patients
        in bed
        """
        patientgen = PatientsGenerator(0, 4, 4, 'a')
        records = patientgen.data.findall('record')
        self.assertEqual(8, len(records),
                         'Incorrect number of records generated')
