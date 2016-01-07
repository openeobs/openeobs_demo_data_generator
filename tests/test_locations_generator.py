import unittest
from demo_data_generators.locations import LocationsGenerator


class TestPatientsGenerator(unittest.TestCase):
    """
    Test that the patients generator does indeed generate patients
    """

    def test_no_update_on_data_element(self):
        """
        Make sure that the data element in the output has the noupdate flag
        set to True
        """
        gen = LocationsGenerator('a', 0)
        no_update = gen.data.attrib['noupdate']
        self.assertEqual(no_update, '1', 'Incorrect noupdate flag')

    def test_creates_ward_record(self):
        """
        Make sure that when no beds defined it just creates the ward record
        """
        gen = LocationsGenerator('a', 0)
        records = gen.data.findall('record')
        self.assertEqual(len(records), 1, 'Incorrect length of ward record')
        record_usage = records[0].find('field[@name=\'usage\']').text
        self.assertEqual(record_usage, 'ward', 'Incorrect record generated')

    def test_creates_bed_record(self):
        """
        Make sure that when no beds defined it just creates the ward record
        """
        gen = LocationsGenerator('a', 1)
        records = gen.data.findall('record')
        self.assertEqual(len(records), 2, 'Incorrect length of ward record')
        record_usage = records[1].find('field[@name=\'usage\']').text
        self.assertEqual(record_usage, 'bed', 'Incorrect record generated')

    def test_non_bed_non_ward_location_code(self):
        """
        Make sure that the non bed non ward code foo works as intended
        """
        gen = LocationsGenerator('a', 0)
        gen.generate_location('a_t1', 'Test', 'test', 'meh', 'a', 1)
        records = gen.data.findall('record')
        self.assertEqual(len(records), 2, 'Incorrect length of ward record')
        record_usage = records[1].find('field[@name=\'code\']').text
        self.assertEqual(record_usage, 'AT1', 'Incorrect record generated')
