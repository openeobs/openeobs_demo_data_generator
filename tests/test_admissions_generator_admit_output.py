import unittest
import re
from demo_data_generators.patients import PatientsGenerator
from demo_data_generators.admissions import AdmissionsGenerator


class TestAdmissionsGeneratorAdmitOutput(unittest.TestCase):
    """
    Test that the admissions generator generates admissions properly
    """

    def setUp(self):
        """
        Setup an example patients generator instance so can use the record
        """
        self.patientgen = PatientsGenerator(0, 1, 0, 'a')
        self.gen = AdmissionsGenerator(self.patientgen, [-1])
        records = self.gen.data.findall('record')
        self.activity_record = records[3]
        self.model_record = records[4]
        self.activity_update_record = records[5]
        eval_regex = r"(\(datetime\.now\(\) \+ timedelta\(-\d\)\)" \
                     r"\.strftime\('%Y-%m-%d %H:%M:%S'\))"
        self.eval_regex = re.compile(eval_regex)

    def test_activity_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.activity_record.attrib['id'],
                         'nhc_activity_demo_admission_0',
                         'Incorrect ID ')
        self.assertEqual(self.activity_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model')

    def test_activity_patient_id_field(self):
        """
        Make sure the patient id field for the  activity is correct
        """
        field = self.activity_record.find('field[@name=\'patient_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_demo_patient_0',
                         'Incorrect patient_id on activity')

    def test_activity_creator_id_field(self):
        """
        Make sure the creator id field for the  activity is correct
        """
        field = self.activity_record.find('field[@name=\'creator_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_activity_demo_adt_admit_0',
                         'Incorrect creator_id on activity')

    def test_activity_parent_id_field(self):
        """
        Make sure the parent id field for the  activity is correct
        """
        field = self.activity_record.find('field[@name=\'parent_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_activity_demo_spell_0',
                         'Incorrect parent_id on activity')

    def test_activity_spell_activity_id_field(self):
        """
        Make sure the spell activity id field for the  activity is correct
        """
        field = self.activity_record.find('field[@name=\'spell_activity_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_activity_demo_spell_0',
                         'Incorrect spell_activity_id on activity')

    def test_activity_state_field(self):
        """
        Make sure the state field for the  activity is correct
        """
        field = self.activity_record.find('field[@name=\'state\']')
        self.assertEqual(field.text, 'completed',
                         'Incorrect state on activity')

    def test_activity_data_model_field(self):
        """
        Make sure the data model field for the  activity is correct
        """
        field = self.activity_record.find('field[@name=\'data_model\']')
        self.assertEqual(field.text, 'nh.clinical.patient.admission',
                         'Incorrect data_model on activity')

    def test_activity_date_terminated_field(self):
        """
        Make sure the date terminated field for the  activity is correct
        """
        field = \
            self.activity_record.find('field[@name=\'date_terminated\']')
        regex_match = re.match(self.eval_regex, field.attrib['eval'])
        self.assertEqual(len(regex_match.groups()), 1,
                         'Incorrect date_started eval on activity')

    def test_model_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.model_record.attrib['id'],
                         'nhc_demo_admission_0',
                         'Incorrect ID ')
        self.assertEqual(self.model_record.attrib['model'],
                         'nh.clinical.patient.admission',
                         'Incorrect model')
    
    def test_activity_id_field(self):
        """
        Make sure the activity_id field for the  is correct
        """
        field = self.model_record.find('field[@name=\'activity_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_activity_demo_admission_0',
                         'Incorrect activity_id on activity')
    
    def test_patient_id_field(self):
        """
        Make sure the patient_id field for the  is correct
        """
        field = self.model_record.find('field[@name=\'patient_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_demo_patient_0',
                         'Incorrect patient_id on activity')
    
    def test_location_id_field(self):
        """
        Make sure the location_id field for the  is correct
        """
        field = self.model_record.find('field[@name=\'location_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_def_conf_location_wa',
                         'Incorrect location_id on activity')
    
    def test_pos_id_field(self):
        """
        Make sure the pos_id field for the  is correct
        """
        field = self.model_record.find('field[@name=\'pos_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_def_conf_pos_hospital',
                         'Incorrect pos_id on activity')
    
    def test_code_field(self):
        """
        Make sure the code field for the  is correct
        """
        field = self.model_record.find('field[@name=\'code\']')
        self.assertEqual(field.text, 'DEMO0000',
                         'Incorrect code on activity')
    
    def test_start_date_field(self):
        """
        Make sure the start_date field for the  is correct
        """
        field = self.model_record.find('field[@name=\'start_date\']')
        regex_match = re.match(self.eval_regex, field.attrib['eval'])
        self.assertEqual(len(regex_match.groups()), 1,
                         'Incorrect start_date eval on activity')
    
    def test_activity_update_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.activity_update_record.attrib['id'],
                         'nhc_activity_demo_admission_0',
                         'Incorrect ID ')
        self.assertEqual(self.activity_update_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model')

    def test_activity_update_data_ref_field(self):
        """
        Make sure the data_ref field for the activity update is correct
        """
        field = self.activity_update_record.find('field[@name=\'data_ref\']')
        self.assertEqual(
            field.attrib['eval'],
            '\'nh.clinical.patient.admission,\' + '
            'str(ref(\'nhc_demo_admission_0\'))',
            'Incorrect data ref on activity update'
        )
