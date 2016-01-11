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
        records = self.gen.data.findall('record')
        self.hospital_location_record = records[0]
        self.admission_location_record = records[1]
        self.discharge_location_record = records[2]
        self.pos_record = records[3]

    def test_hospital_location_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.hospital_location_record.attrib['id'],
                         'nhc_def_conf_location_guh',
                         'Incorrect ID ')
        self.assertEqual(self.hospital_location_record.attrib['model'],
                         'nh.clinical.location',
                         'Incorrect model')

    def test_hospital_location_name_field(self):
        """
        Make sure the name field is correct
        """
        field = self.hospital_location_record.find('field[@name=\'name\']')
        self.assertEqual(field.text, 'GUH POS Location',
                         'Incorrect name on location')
        
    def test_hospital_location_code_field(self):
        """
        Make sure the code field is correct
        """
        field = self.hospital_location_record.find('field[@name=\'code\']')
        self.assertEqual(field.text, 'GUH',
                         'Incorrect code on location')
        
    def test_hospital_location_type_field(self):
        """
        Make sure the type field is correct
        """
        field = self.hospital_location_record.find('field[@name=\'type\']')
        self.assertEqual(field.text, 'pos',
                         'Incorrect type on location')

    def test_hospital_location_usage_field(self):
        """
        Make sure the usage field is correct
        """
        field = self.hospital_location_record.find('field[@name=\'usage\']')
        self.assertEqual(field.text, 'hospital',
                         'Incorrect usage on location')
        
    def test_admission_location_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.admission_location_record.attrib['id'],
                         'nhc_def_conf_location_lot_admission',
                         'Incorrect ID ')
        self.assertEqual(self.admission_location_record.attrib['model'],
                         'nh.clinical.location',
                         'Incorrect model')

    def test_admission_location_name_field(self):
        """
        Make sure the name field is correct
        """
        field = self.admission_location_record.find('field[@name=\'name\']')
        self.assertEqual(field.text, 'Admission Location',
                         'Incorrect name on location')
        
    def test_admission_location_code_field(self):
        """
        Make sure the code field is correct
        """
        field = self.admission_location_record.find('field[@name=\'code\']')
        self.assertEqual(field.text, 'ADML-GUH',
                         'Incorrect code on location')
        
    def test_admission_location_type_field(self):
        """
        Make sure the type field is correct
        """
        field = self.admission_location_record.find('field[@name=\'type\']')
        self.assertEqual(field.text, 'structural',
                         'Incorrect type on location')

    def test_admission_location_usage_field(self):
        """
        Make sure the usage field is correct
        """
        field = self.admission_location_record.find('field[@name=\'usage\']')
        self.assertEqual(field.text, 'room',
                         'Incorrect usage on location')
        
    def test_admission_location_parent_field(self):
        """
        Make sure the parent field is correct
        """
        field = \
            self.admission_location_record.find('field[@name=\'parent_id\']')
        self.assertEqual(field.attrib['ref'],
                         'nhc_def_conf_location_guh',
                         'Incorrect parent id')

    def test_discharge_location_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.discharge_location_record.attrib['id'],
                         'nhc_def_conf_location_lot_discharge',
                         'Incorrect ID ')
        self.assertEqual(self.discharge_location_record.attrib['model'],
                         'nh.clinical.location',
                         'Incorrect model')

    def test_discharge_location_name_field(self):
        """
        Make sure the name field is correct
        """
        field = self.discharge_location_record.find('field[@name=\'name\']')
        self.assertEqual(field.text, 'Discharge Location',
                         'Incorrect name on location')
        
    def test_discharge_location_code_field(self):
        """
        Make sure the code field is correct
        """
        field = self.discharge_location_record.find('field[@name=\'code\']')
        self.assertEqual(field.text, 'DISL-GUH',
                         'Incorrect code on location')
        
    def test_discharge_location_type_field(self):
        """
        Make sure the type field is correct
        """
        field = self.discharge_location_record.find('field[@name=\'type\']')
        self.assertEqual(field.text, 'structural',
                         'Incorrect type on location')

    def test_discharge_location_usage_field(self):
        """
        Make sure the usage field is correct
        """
        field = self.discharge_location_record.find('field[@name=\'usage\']')
        self.assertEqual(field.text, 'room',
                         'Incorrect usage on location')
        
    def test_discharge_location_parent_field(self):
        """
        Make sure the parent field is correct
        """
        field = \
            self.discharge_location_record.find('field[@name=\'parent_id\']')
        self.assertEqual(field.attrib['ref'],
                         'nhc_def_conf_location_guh',
                         'Incorrect parent id')

    def test_pos_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.pos_record.attrib['id'],
                         'nhc_def_conf_pos_hospital',
                         'Incorrect ID ')
        self.assertEqual(self.pos_record.attrib['model'],
                         'nh.clinical.pos',
                         'Incorrect model')

    def test_pos_record_name_field(self):
        """
        Make sure the name field is correct
        """
        field = self.pos_record.find('field[@name=\'name\']')
        self.assertEqual(field.text, 'Greenfield University Hospital',
                         'Incorrect name on location')

    def test_pos_record_location_field(self):
        """
        Make sure the location field is correct
        """
        field = self.pos_record.find('field[@name=\'location_id\']')
        self.assertEqual(field.attrib['ref'],
                         'nhc_def_conf_location_guh',
                         'Incorrect location id')

    def test_pos_record_company_field(self):
        """
        Make sure the company field is correct
        """
        field = self.pos_record.find('field[@name=\'company_id\']')
        self.assertEqual(field.attrib['ref'],
                         'base.main_company',
                         'Incorrect company id')

    def test_pos_record_lot_admission_field(self):
        """
        Make sure the lot admission id field is correct
        """
        field = \
            self.pos_record.find('field[@name=\'lot_admission_id\']')
        self.assertEqual(field.attrib['ref'],
                         'nhc_def_conf_location_lot_admission',
                         'Incorrect lot admission id')

    def test_pos_record_lot_discharge_field(self):
        """
        Make sure the lot discharge id field is correct
        """
        field = \
            self.pos_record.find('field[@name=\'lot_discharge_id\']')
        self.assertEqual(field.attrib['ref'],
                         'nhc_def_conf_location_lot_discharge',
                         'Incorrect lot discharge id')
