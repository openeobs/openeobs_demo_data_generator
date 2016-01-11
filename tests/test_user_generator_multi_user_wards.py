import unittest
from demo_data_generators.users import UsersGenerator


class TestUserGeneratorMultiUserWards(unittest.TestCase):

    def test_multi_wards_with_empty_user_schema(self):
        """
        Test that multiwards doesn't do anything if no user schema defined
        """
        gen = UsersGenerator({})
        gen.generate_multi_wards_users(['a', 'b', 'c', 'd', 'e'])
        xml = gen.class_data
        records = xml.findall('record')
        self.assertEqual(len(records), 0, 'Incorrect number of records')

    def test_multi_wards_with_one_multi_ward_user(self):
        """
        Test that when only one user is a multiward user that only one record
        is generated
        """
        schema = {
            'ward_manager': {
                'total': 2,
                'per_ward': 1,
                'unassigned': 0,
                'multi_wards': [['a', 'b'], []]
            }
        }
        gen = UsersGenerator(schema)
        gen.generate_multi_wards_users(['a', 'b'])
        xml = gen.class_data
        records = xml.findall('record')
        self.assertEqual(len(records), 2, 'Incorrect number of records')
        multi_record = records[0]
        no_multi_record = records[1]
        multi_locations = multi_record.find('field[@name=\'location_ids\']')
        no_locations = no_multi_record.find('field[@name=\'location_ids\']')
        self.assertEqual(
            multi_locations.attrib['eval'],
            '[[6, False, [ref(\'nhc_def_conf_location_wa\'),'
            'ref(\'nhc_def_conf_location_wb\')]]]',
            'Incorrect Location ids for multiple wards'
        )
        self.assertEqual(no_locations.attrib['eval'], '[[6, False, []]]',
                         'Incorrect Location ids for single wards')

    def test_multi_wards_with_all_multi_ward_user(self):
        """
        Test that when only one user is a multiward user that only one record
        is generated
        """
        schema = {
            'ward_manager': {
                'total': 2,
                'per_ward': 1,
                'unassigned': 0,
                'multi_wards': 'all'
            }
        }
        gen = UsersGenerator(schema)
        gen.generate_multi_wards_users(['a', 'b'])
        xml = gen.class_data
        records = xml.findall('record')
        self.assertEqual(len(records), 2, 'Incorrect number of records')
        multi_record_one = records[0]
        multi_record_two = records[1]
        one_locations = multi_record_one.find('field[@name=\'location_ids\']')
        two_locations = multi_record_two.find('field[@name=\'location_ids\']')
        self.assertEqual(
            one_locations.attrib['eval'],
            '[[6, False, [ref(\'nhc_def_conf_location_wa\'),'
            'ref(\'nhc_def_conf_location_wb\')]]]',
            'Incorrect Location ids for multiple wards'
        )
        self.assertEqual(
            two_locations.attrib['eval'],
            '[[6, False, [ref(\'nhc_def_conf_location_wa\'),'
            'ref(\'nhc_def_conf_location_wb\')]]]',
            'Incorrect Location ids for multiple wards'
        )
