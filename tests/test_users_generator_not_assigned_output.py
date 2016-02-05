import unittest
from demo_data_generators.users import UsersGenerator


class TestUsersGeneratorMultiWardOutput(unittest.TestCase):
    """
    Test that the users generator generates the multiple ward output correctly
    """

    def setUp(self):
        """
        Setup an example users generator instance so can use the record
        """
        john_schema = {  # http://cdn.makeagif.com/media/9-13-2015/28JfPx.gif
            'nurse': {
                'total': 1,
                'per_ward': 0,
                'unassigned': 1,
                'multi_wards': [[]]
            }
        }
        gen = UsersGenerator(john_schema)
        gen.names_generators['nurse'] = (n for n in ['Nadine'])
        gen.generate_users_not_assigned()
        self.record = gen.class_data.findall('record')[0]

    def test_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.record.attrib['id'],
                         'nhc_def_conf_nurse_nadine_user',
                         'Incorrect ID ')
        self.assertEqual(self.record.attrib['model'],
                         'res.users',
                         'Incorrect model')

    def test_name_field(self):
        """
        Make sure the name field is correct
        """
        field = self.record.find('field[@name=\'name\']')
        self.assertTrue('Nadine' in field.text, 'Incorrect Name Field')

    def test_login_field(self):
        """
        Make sure the login field is correct
        """
        field = self.record.find('field[@name=\'login\']')
        self.assertEqual(field.text, 'nadine', 'Incorrect login Field')

    def test_password_field(self):
        """
        Make sure the password field is correct
        """
        field = self.record.find('field[@name=\'password\']')
        self.assertEqual(field.text, 'nadine', 'Incorrect password Field')

    def test_timezone_field(self):
        """
        Make sure the tz field is correct
        """
        field = self.record.find('field[@name=\'tz\']')
        self.assertEqual(field.text, 'Europe/London',
                         'Incorrect timezone Field')

    def test_group_field(self):
        """
        Make sure the login field is correct
        """
        field = self.record.find('field[@name=\'groups_id\']')
        self.assertEqual(field.attrib['eval'],
                         '[(4, ref(\'nh_clinical.group_nhc_nurse\'))]',
                         'Incorrect eval on groups id')

    def test_category_field(self):
        """
        Make sure the category field is correct
        """
        field = self.record.find('field[@name=\'category_id\']')
        self.assertEqual(field.attrib['eval'],
                         '[(4, ref(\'nh_clinical.role_nhc_nurse\'))]',
                         'Incorrect eval on category id')

    def test_locations_field(self):
        """
        Make sure the locations field is correct
        """
        field = self.record.find('field[@name=\'location_ids\']')
        self.assertEqual(
            field.attrib['eval'],
            '[[6, False, []]]',
            'Incorrect eval on location ids'
        )

    def test_pos_field(self):
        """
        Make sure the pos field is correct
        """
        field = self.record.find('field[@name=\'pos_ids\']')
        self.assertEqual(
            field.attrib['eval'],
            "[[6,0,[ref('nh_clinical.nhc_location_default_pos')]]]")
