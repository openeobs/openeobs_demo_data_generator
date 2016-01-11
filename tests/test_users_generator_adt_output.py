import unittest
from demo_data_generators.users import UsersGenerator


class TestUsersGeneratorADTOutput(unittest.TestCase):
    """
    Test that the users generator does indeed generate the adt user
    """

    def setUp(self):
        """
        Setup an example users generator instance so can use the record
        """
        gen = UsersGenerator({})
        gen.generate_adt_user()
        self.record = gen.class_data.findall('record')[0]

    def test_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.record.attrib['id'],
                         'nhc_def_conf_adt_user',
                         'Incorrect ID ')
        self.assertEqual(self.record.attrib['model'],
                         'res.users',
                         'Incorrect model')

    def test_name_field(self):
        """
        Make sure the name field is correct
        """
        field = self.record.find('field[@name=\'name\']')
        self.assertEqual(field.text, 'GUH-ADT', 'Incorrect Name Field')

    def test_login_field(self):
        """
        Make sure the login field is correct
        """
        field = self.record.find('field[@name=\'login\']')
        self.assertEqual(field.text, 'adt', 'Incorrect login Field')

    def test_password_field(self):
        """
        Make sure the password field is correct
        """
        field = self.record.find('field[@name=\'password\']')
        self.assertEqual(field.text, 'adt', 'Incorrect password Field')

    def test_group_field(self):
        """
        Make sure the login field is correct
        """
        field = self.record.find('field[@name=\'groups_id\']')
        self.assertEqual(field.attrib['eval'],
                         '[(4, ref(\'nh_clinical.group_nhc_admin\'))]',
                         'Incorrect eval on groups id')

    def test_category_field(self):
        """
        Make sure the category field is correct
        """
        field = self.record.find('field[@name=\'category_id\']')
        self.assertEqual(field.attrib['eval'],
                         '[(4, ref(\'nh_clinical.role_nhc_admin\'))]',
                         'Incorrect eval on category id')

    def test_pos_field(self):
        """
        Make sure the pos field is correct
        """
        field = self.record.find('field[@name=\'pos_id\']')
        self.assertEqual(field.attrib['ref'],
                         'nhc_def_conf_pos_hospital',
                         'Incorrect eval on pos id')
