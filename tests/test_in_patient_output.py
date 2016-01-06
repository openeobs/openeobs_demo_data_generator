import unittest
from datetime import datetime
from demo_data_generators.patients import PatientsGenerator


class TestInBedPatientOutput(unittest.TestCase):
    """
    Test that the patients generator does indeed generate patients
    """

    def setUp(self):
        """
        Setup an example patients generator instance so can use the record
        """
        patientgen = PatientsGenerator(0, 1, 0, 'a')
        self.record = patientgen.data.find('record')
        self.gender_sex = patientgen.gender_sex_list
        self.ethnicities = patientgen.ethnicity_list
        # self.female_names = patientgen.data_generator.first_names_female
        # self.male_names = patientgen.data_generator.first_names_male
        # self.last_names = patientgen.data_generator.last_names

    def test_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.record.attrib['id'],
                         'nhc_demo_patient_0',
                         'Incorrect ID ')
        self.assertEqual(self.record.attrib['model'],
                         'nh.clinical.patient',
                         'Incorrect model')

    def test_dob_field(self):
        """
        Make sure the date of birth field is correct
        """
        dob_field = self.record.find('field[@name=\'dob\']')
        dob_date = datetime.strptime(dob_field.text, '%Y-%m-%d %H:%M:%S')
        self.assertTrue(isinstance(dob_date, datetime), 'Date isn\'t correct')

    def test_gender_sex(self):
        """
        Make sure that the gender and sex selection is in the options and both
        as the same
        """
        gender_field = self.record.find('field[@name=\'gender\']')
        sex_field = self.record.find('field[@name=\'sex\']')
        self.assertIn(gender_field.text, self.gender_sex,
                      'Gender not in selection')
        self.assertIn(sex_field.text, self.gender_sex,
                      'Sex not in selection')
        self.assertEqual(gender_field.text, sex_field.text,
                         'Gender and Sex are not the same')

    def test_ethnicity(self):
        """
        Make sure that the ethnicity is in the ethnicity list
        """
        ethnicity_field = self.record.find('field[@name=\'ethnicity\']')
        self.assertIn(ethnicity_field.text, self.ethnicities,
                      'Ethnicity not in the options')

    def test_patient_identifier(self):
        """
        Make sure the patient identifier is in NHSNUM0000
        """
        patient_id_field = \
            self.record.find('field[@name=\'patient_identifier\']')
        self.assertEqual(patient_id_field.text, 'NHSNUM0000',
                         'Patient Identifier incorrect')
        
    def test_other_identifier(self):
        """
        Make sure the other identifier is in HOSNUM0000
        """
        other_id_field = \
            self.record.find('field[@name=\'other_identifier\']')
        self.assertEqual(other_id_field.text, 'HOSNUM0000',
                         'other Identifier incorrect')

    # def test_given_name(self):
    #     """
    #     Make sure the given name is in the list
    #     """
    #     given_name_field = self.record.find('field[@name=\'given_name\']')
    #     sex_field = self.record.find('field[@name=\'sex\']')
    #     if sex_field.text == 'F':
    #         self.assertIn(given_name_field.text, self.female_names,
    #                       'Incorrect given name')
    #     if sex_field.text == 'M':
    #         self.assertIn(given_name_field.text, self.male_names,
    #                       'Incorrect given name')
    #
    # def test_middle_name(self):
    #     """
    #     Make sure the middle name is in the list
    #     """
    #     middle_name_field = self.record.find('field[@name=\'middle_name\']')
    #     sex_field = self.record.find('field[@name=\'sex\']')
    #     if sex_field.text == 'F':
    #         self.assertIn(middle_name_field.text, self.female_names,
    #                       'Incorrect given name')
    #     if sex_field.text == 'M':
    #         self.assertIn(middle_name_field.text, self.male_names,
    #                       'Incorrect given name')
    #
    # def test_last_name(self):
    #     """
    #     Make sure the middle name is in the list
    #     """
    #     last_name_field = self.record.find('field[@name=\'last_name\']')
    #     self.assertIn(last_name_field.text, self.last_names,
    #                   'Incorrect given name')

    def test_current_location_id_bed(self):
        """
        Make sure the current location id is the bed
        """
        bed_field = self.record.find('field[@name=\'current_location_id\']')
        self.assertEqual(bed_field.attrib['ref'],
                         'nhc_def_conf_location_wa_b1',
                         'Incorrect bed defined')

    def test_current_location_id_ward(self):
        """
        Make sure the current location id is the bed
        """
        ward_data = PatientsGenerator(0, 0, 1, 'a')
        record = ward_data.data.find('record')
        bed_field = record.find('field[@name=\'current_location_id\']')
        self.assertEqual(bed_field.attrib['ref'],
                         'nhc_def_conf_location_wa',
                         'Incorrect bed defined')