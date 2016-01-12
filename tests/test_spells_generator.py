import unittest
import re
from demo_data_generators.spells import SpellsGenerator
from demo_data_generators.patients import PatientsGenerator


class TestSpellsGenerator(unittest.TestCase):
    """
    Test that the spells generator does indeed generate spells
    """

    def setUp(self):
        """
        As SpellsGenerator needs the output of the an instance of
        PatientsGenerator need to create ourselves an instance
        """
        bed_patient = PatientsGenerator(0, 1, 0, 'a')
        self.spellgen = SpellsGenerator(bed_patient, [-1])

    def test_no_update_on_data_element(self):
        """
        Make sure that the data element in the output has the noupdate flag
        set to True
        """
        no_update = self.spellgen.data.attrib['noupdate']
        self.assertEqual(no_update, '1', 'Incorrect noupdate flag')

    def test_has_admit_date_eval_string(self):
        """
        Make sure that it has a string that can be used for the eval attribute
        on elements for the date admitted
        """
        eval_string = '(datetime.now() + timedelta({0}))' \
                      '.strftime(\'%Y-%m-%d %H:%M:%S\')'
        self.assertEqual(self.spellgen.admit_date_eval_string, eval_string,
                         'Incorrect Admit date eval string List')
        
    def test_has_patient_id_regex(self):
        """
        Make sure that the patient_id regex is valid
        """
        patient_id_groups = re.match(self.spellgen.patient_id_regex,
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
        records = self.spellgen.data.findall('record')
        self.assertEqual(3, len(records),
                         'Incorrect number of records generated')

    def test_records_for_spell(self):
        """
        Make sure that it generates the right models for records for the spell
        """
        records = self.spellgen.data.findall('record')
        activity_spell_record = records[0]
        spell_record = records[1]
        activity_update_record = records[2]
        self.assertEqual(activity_spell_record.attrib['model'], 'nh.activity',
                         'Incorrect model for activity spell record')
        self.assertEqual(spell_record.attrib['model'], 'nh.clinical.spell',
                         'Inccorect model for spell record')
        self.assertEqual(activity_update_record.attrib['model'], 'nh.activity',
                         'Incorrect model for activity spell record update')
