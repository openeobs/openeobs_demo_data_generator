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
            'ward_manager': {
                'total': 1,
                'per_ward': 1,
                'unassigned': 0,
                'multi_wards': [['a', 'b']]
            }
        }
        gen = UsersGenerator(john_schema)
        gen.names_generators['ward_manager'] = (n for n in ['Waino'])
        gen.generate_multi_wards_users(['a'])
        self.record = gen.class_data.findall('record')[0]

    def test_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.record.attrib['id'],
                         'nhc_def_conf_ward_manager_waino_user',
                         'Incorrect ID ')
        self.assertEqual(self.record.attrib['model'],
                         'res.users',
                         'Incorrect model')

    def test_name_field(self):
        """
        Make sure the name field is correct
        """
        field = self.record.find('field[@name=\'name\']')
        self.assertTrue('Waino' in field.text, 'Incorrect Name Field')

    def test_login_field(self):
        """
        Make sure the login field is correct
        """
        field = self.record.find('field[@name=\'login\']')
        self.assertEqual(field.text, 'waino', 'Incorrect login Field')

    def test_password_field(self):
        """
        Make sure the password field is correct
        """
        field = self.record.find('field[@name=\'password\']')
        self.assertEqual(field.text, 'waino', 'Incorrect password Field')

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
                         '[(4, ref(\'nh_clinical.group_nhc_ward_manager\'))]',
                         'Incorrect eval on groups id')

    def test_category_field(self):
        """
        Make sure the category field is correct
        """
        field = self.record.find('field[@name=\'category_id\']')
        self.assertEqual(field.attrib['eval'],
                         '[(4, ref(\'nh_clinical.role_nhc_ward_manager\'))]',
                         'Incorrect eval on category id')

    def test_locations_field(self):
        """
        Make sure the locations field is correct
        """
        field = self.record.find('field[@name=\'location_ids\']')
        self.assertEqual(field.attrib['eval'],
                         '[[6, False, [ref(\'nhc_def_conf_location_wa\'),'
                         'ref(\'nhc_def_conf_location_wb\')]]]',
                         'Incorrect eval on location ids')

    def test_pos_field(self):
        """
        Make sure the pos field is correct
        """
        field = self.record.find('field[@name=\'pos_ids\']')
        self.assertEqual(
            field.attrib['eval'],
            "[[6,0,[ref('nh_clinical.nhc_location_default_pos')]]]")
