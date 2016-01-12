"""Test that the admissions generator does indeed generate admissions"""
import unittest
import re
from demo_data_generators.admissions import AdmissionsGenerator
from demo_data_generators.patients import PatientsGenerator


class TestAdmissionsGenerator(unittest.TestCase):
    """
    Test that the admissions generator does indeed generate admissions
    """

    def setUp(self):
        """
        As SpellsGenerator needs the output of the an instance of
        PatientsGenerator need to create ourselves an instance
        """
        bed_patient = PatientsGenerator(0, 1, 0, 'a')
        self.admitgen = AdmissionsGenerator(bed_patient, [-1])

    def test_no_update_on_data_element(self):
        """
        Make sure that the data element in the output has the noupdate flag
        set to True
        """
        no_update = self.admitgen.data.attrib['noupdate']
        self.assertEqual(no_update, '1', 'Incorrect noupdate flag')

    def test_has_admit_date_eval_string(self):
        """
        Make sure that it has a string that can be used for the eval attribute
        on elements for the date admitted
        """
        eval_string = '(datetime.now() + timedelta({0}))' \
                      '.strftime(\'%Y-%m-%d %H:%M:%S\')'
        self.assertEqual(self.admitgen.admit_date_eval_string, eval_string,
                         'Incorrect Admit date eval string List')

    def test_has_ward_regex(self):
        """
        Make sure that the ward regex is valid
        """
        ward_groups = re.match(self.admitgen.ward_regex,
                               'nhc_def_conf_location_wa')
        self.assertEqual(len(ward_groups.groups()), 1,
                         'Incorrect regex groups')
        self.assertEqual(ward_groups.groups()[0], 'nhc_def_conf_location_wa',
                         'Incorrect Regex match')

    def test_has_patient_id_regex(self):
        """
        Make sure that the patient_id regex is valid
        """
        patient_id_groups = re.match(self.admitgen.patient_id_regex,
                                     'nhc_demo_patient_666')
        self.assertEqual(len(patient_id_groups.groups()), 1,
                         'Incorrect regex groups')
        self.assertEqual(patient_id_groups.groups()[0],
                         '666',
                         'Incorrect Regex match')

    def test_number_of_records_for_spell(self):
        """
        Make sure that it generates the number of records for the spell
        """
        records = self.admitgen.data.findall('record')
        self.assertEqual(9, len(records),
                         'Incorrect number of records generated')

    def test_adt_admit_records_for_spell(self):
        """
        Make sure that it generates the right models for records for the spell
        """
        records = self.admitgen.data.findall('record')
        adt_admit_activity_record = records[0]
        adt_admit_record = records[1]
        adt_admit_activity_update_record = records[2]
        self.assertEqual(adt_admit_activity_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model for adt admit activity record')
        self.assertEqual(adt_admit_record.attrib['model'],
                         'nh.clinical.adt.patient.admit',
                         'Inccorect model for adt admit record')
        self.assertEqual(adt_admit_activity_update_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model for activity update record update')

    def test_admit_records_for_spell(self):
        """
        Make sure that it generates the right models for records for the spell
        """
        records = self.admitgen.data.findall('record')
        admit_activity_record = records[3]
        admit_record = records[4]
        admit_activity_update_record = records[5]
        self.assertEqual(admit_activity_record.attrib['model'], 'nh.activity',
                         'Incorrect model for admit activity record')
        self.assertEqual(admit_record.attrib['model'],
                         'nh.clinical.patient.admission',
                         'Inccorect model for admit record')
        self.assertEqual(admit_activity_update_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model for update activity record update')

    def test_movement_records_for_spell(self):
        """
        Make sure that it generates the right models for records for the spell
        """
        records = self.admitgen.data.findall('record')
        movement_activity_record = records[6]
        movement_record = records[7]
        movement_activity_update_record = records[8]
        self.assertEqual(movement_activity_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model for activity movement record')
        self.assertEqual(movement_record.attrib['model'],
                         'nh.clinical.patient.move',
                         'Inccorect model for movement record')
        self.assertEqual(movement_activity_update_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model for activity update record update')
