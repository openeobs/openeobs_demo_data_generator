import unittest
import re
from demo_data_generators.placements import PlacementsGenerator
from demo_data_generators.patients import PatientsGenerator


class TestPlacementsGenerator(unittest.TestCase):
    """
    Test that the admissions generator does indeed generate admissions
    """

    def setUp(self):
        """
        As SpellsGenerator needs the output of the an instance of
        PatientsGenerator need to create ourselves an instance
        """
        bed_patient = PatientsGenerator(0, 1, 0, 'a')
        self.gen = PlacementsGenerator(bed_patient)

    def test_has_admit_offset_list(self):
        """
        Generator has an admit offset list
        """
        offset_list = ['-1', '-2']
        self.assertEqual(offset_list, self.gen.admit_offset_list,
                         'Admit offset list incorrect')

    def test_no_update_on_data_element(self):
        """
        Make sure that the data element in the output has the noupdate flag
        set to True
        """
        no_update = self.gen.data.attrib['noupdate']
        self.assertEqual(no_update, '1', 'Incorrect noupdate flag')

    def test_has_admit_date_eval_string(self):
        """
        Make sure that it has a string that can be used for the eval attribute
        on elements for the date admitted
        """
        eval_string = '(datetime.now() + timedelta({0}))' \
                      '.strftime(\'%Y-%m-%d %H:%M:%S\')'
        self.assertEqual(self.gen.admit_date_eval_string, eval_string,
                         'Incorrect Admit date eval string List')

    def test_has_ward_regex(self):
        """
        Make sure that the ward regex is valid
        """
        ward_groups = re.match(self.gen.ward_regex,
                               'nhc_def_conf_location_wa')
        self.assertEqual(len(ward_groups.groups()), 1,
                         'Incorrect regex groups')
        self.assertEqual(ward_groups.groups()[0], 'nhc_def_conf_location_wa',
                         'Incorrect Regex match')
        
    def test_has_patient_id_regex(self):
        """
        Make sure that the patient_id regex is valid
        """
        patient_id_groups = re.match(self.gen.patient_id_regex,
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
        records = self.gen.data.findall('record')
        self.assertEqual(6, len(records),
                         'Incorrect number of records generated')

    def test_placement_records_for_spell(self):
        """
        Make sure that it generates the right models for records for the spell
        """
        records = self.gen.data.findall('record')
        placement_activity_record = records[0]
        placement_record = records[1]
        placement_activity_update_record = records[2]
        self.assertEqual(placement_activity_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model for placement activity record')
        self.assertEqual(placement_record.attrib['model'],
                         'nh.clinical.patient.placement',
                         'Inccorect model for placement record')
        self.assertEqual(placement_activity_update_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model for update activity record update')

    def test_movement_records_for_spell(self):
        """
        Make sure that it generates the right models for records for the spell
        """
        records = self.gen.data.findall('record')
        movement_activity_record = records[3]
        movement_record = records[4]
        movement_activity_update_record = records[5]
        self.assertEqual(movement_activity_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model for activity movement record')
        self.assertEqual(movement_record.attrib['model'],
                         'nh.clinical.patient.move',
                         'Inccorect model for movement record')
        self.assertEqual(movement_activity_update_record.attrib['model'],
                         'nh.activity',
                         'Incorrect model for activity update record update')
