import unittest
from demo_data_generators.users import UsersGenerator


class TestUserGeneratorUsersPerWard(unittest.TestCase):

    def test_users_per_ward_with_empty_user_schema(self):
        """
        Test that doesn't do anything if no user schema defined
        """
        gen = UsersGenerator({})
        doc = gen.generate_users_per_ward('a', 666)
        xml = doc.findall('data')[0]
        records = xml.findall('record')
        self.assertEqual(len(records), 0, 'Incorrect number of records')

    def test_user_per_ward_with_no_user_per_ward(self):
        """
        Test that doesn't do anything if no users by ward
        """
        basic_schema = {
            'hca': {
                'total': 666,
                'per_ward': 0,
                'unassigned': 666,
            }
        }
        gen = UsersGenerator(basic_schema)
        doc = gen.generate_users_per_ward('a', 666)
        xml = doc.findall('data')[0]
        records = xml.findall('record')
        self.assertEqual(len(records), 0, 'Incorrect number of records')

    def test_user_per_ward_with_bed_assignable_user(self):
        """
        Test that assigns user to bed when bed assignable
        """
        basic_schema = {
            'hca': {
                'total': 1,
                'per_ward': 1,
                'unassigned': 0,
            }
        }
        gen = UsersGenerator(basic_schema)
        doc = gen.generate_users_per_ward('a', 2)
        xml = doc.findall('data')[0]
        records = xml.findall('record')
        self.assertEqual(len(records), 1, 'Incorrect number of records')
        record = records[0]
        location = record.find('field[@name=\'location_ids\']')
        self.assertEqual(
            location.attrib['eval'],
            '[[6, False, [ref(\'nhc_def_conf_location_wa_b1\'),'
            'ref(\'nhc_def_conf_location_wa_b2\')]]]',
            'Incorrect Location ids for user per ward'
        )

    def test_user_per_ward_with_ward_assignable_user(self):
        """
        Test that assigns user to bed when bed assignable
        """
        basic_schema = {
            'ward_manager': {
                'total': 1,
                'per_ward': 1,
                'unassigned': 0,
            }
        }
        gen = UsersGenerator(basic_schema)
        doc = gen.generate_users_per_ward('a', 2)
        xml = doc.findall('data')[0]
        records = xml.findall('record')
        self.assertEqual(len(records), 1, 'Incorrect number of records')
        record = records[0]
        location = record.find('field[@name=\'location_ids\']')
        self.assertEqual(
            location.attrib['eval'],
            '[[6, False, [ref(\'nhc_def_conf_location_wa\')]]]',
            'Incorrect Location ids for user per ward'
        )

    def test_user_per_ward_with_non_bed_ward_assignable_user(self):
        """
        Test that assigns user to bed when bed assignable
        """
        basic_schema = {
            'senior_manager': {
                'total': 1,
                'per_ward': 1,
                'unassigned': 0,
            }
        }
        gen = UsersGenerator(basic_schema)
        doc = gen.generate_users_per_ward('a', 2)
        xml = doc.findall('data')[0]
        records = xml.findall('record')
        self.assertEqual(len(records), 1, 'Incorrect number of records')
        record = records[0]
        location = record.find('field[@name=\'location_ids\']')
        self.assertEqual(
            location.attrib['eval'],
            '[[6, False, []]]',
            'Incorrect Location ids for user per ward'
        )

