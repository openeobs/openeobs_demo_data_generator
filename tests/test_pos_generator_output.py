import unittest
from demo_data_generators.pos import POSGenerator


class TestPOSGeneratorOutput(unittest.TestCase):
    """
    Test that the spells generator generates spells properly
    """

    def setUp(self):
        """
        Setup an example patients generator instance so can use the record
        """
        self.gen = POSGenerator()
        records = self.gen.data
        self.pos_record = records[1]
        self.hospital_location_record = records[0]

    def test_hospital_location_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.hospital_location_record.attrib['id'],
                         'nh_clinical.nhc_location_default_hospital')
        self.assertEqual(self.hospital_location_record.attrib['model'],
                         'nh.clinical.location')

    def test_hospital_location_type_field(self):
        """
        Make sure the type field is correct
        """
        field = self.hospital_location_record.find('field[@name=\'type\']')
        self.assertEqual(field.text, 'pos')

    def test_hospital_location_usage_field(self):
        """
        Make sure the usage field is correct
        """
        field = self.hospital_location_record.find('field[@name=\'usage\']')
        self.assertEqual(field.text, 'hospital')

    def test_pos_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(
            self.pos_record.attrib['id'],
            'nh_clinical.nhc_location_default_pos')
        self.assertEqual(
            self.pos_record.attrib['model'], 'nh.clinical.pos')

    def test_pos_record_name_field(self):
        """
        Make sure the name field is correct
        """
        field = self.pos_record.find('field[@name=\'name\']')
        self.assertEqual(field.text, 'Greenfield University Hospital')

    def test_pos_record_location_field(self):
        """
        Make sure the location field is correct
        """
        field = self.pos_record.find('field[@name=\'location_id\']')
        self.assertEqual(field.attrib['ref'],
                         'nh_clinical.nhc_location_default_hospital')

    def test_pos_record_company_field(self):
        """
        Make sure the company field is correct
        """
        field = self.pos_record.find('field[@name=\'company_id\']')
        self.assertEqual(field.attrib['ref'], 'base.main_company')

