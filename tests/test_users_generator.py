import unittest
from demo_data_generators.users import UsersGenerator


class TestUsersGenerator(unittest.TestCase):
    """
    Test that the patients generator does indeed generate patients
    """

    def test_has_timezone(self):
        """
        generator has an timezone property, make sure it def does
        """
        gen = UsersGenerator({})
        timezone = 'Europe/London'
        self.assertEqual(timezone, gen.timezone,
                         'Timezone incorrect')

    def test_no_update_on_data_element(self):
        """
        Make sure that the class_data element in the output has the
        noupdate flag set to True
        """
        gen = UsersGenerator({})
        no_update = gen.class_data.attrib['noupdate']
        self.assertEqual(no_update, '1', 'Incorrect noupdate flag')

    def test_has_user_groups(self):
        """
        Make sure that the class has a user groups dictionary
        """
        gen = UsersGenerator({})
        user_groups = {
            'hca': 'group_nhc_hca',
            'nurse': 'group_nhc_nurse',
            'ward_manager': 'group_nhc_ward_manager',
            'senior_manager': 'group_nhc_senior_manager',
            'doctor': 'group_nhc_doctor',
            'kiosk': 'group_nhc_kiosk',
            'admin': 'group_nhc_admin'
        }
        self.assertEqual(user_groups, gen.groups,
                         'Incorrect User Group Dictionary')

    def test_has_user_roles(self):
        """
        Make sure that the class has a user roles dictionary
        """
        gen = UsersGenerator({})
        user_roles = {
            'hca': 'role_nhc_hca',
            'nurse': 'role_nhc_nurse',
            'ward_manager': 'role_nhc_ward_manager',
            'senior_manager': 'role_nhc_senior_manager',
            'doctor': 'role_nhc_doctor',
            'kiosk': 'role_nhc_kiosk',
            'admin': 'role_nhc_admin'
        }
        self.assertEqual(user_roles, gen.categories,
                         'Incorrect User Role Dictionary')

    def test_has_tuple_of_users_assignable_to_ward(self):
        """
        Make sure that the class has a tuple for users assignable to wards
        """
        gen = UsersGenerator({})
        ward_assignable = (
            'ward_manager',
            'doctor',
            'kiosk',
        )
        self.assertEqual(ward_assignable, gen.assignable_to_ward,
                         'Incorrect data on users assignable to a ward')

    def test_has_tuple_of_users_assignable_to_bed(self):
        """
        Make sure that the class has a tuple for users assignable to beds
        """
        gen = UsersGenerator({})
        bed_assignable = (
            'hca',
            'nurse',
        )
        self.assertEqual(bed_assignable, gen.assignable_to_bed,
                         'Incorrect data on users assignable to a bed')

    def test_has_user_schema_empty(self):
        """
        Make sure that the class holds the user schema passed
        """
        gen = UsersGenerator({})
        self.assertEqual(gen.users_schema, {}, 'Incorrect User Schema stored')

    def test_has_user_schema_basic(self):
        """
        Make sure that the class holds the user schema passed
        """
        basic_schema = {
            'hca': {
                'total': 0,
                'per_ward': 0,
                'unassigned': 0,
                'multi_wards': 0
            },
            'nurse': {
                'total': 0,
                'per_ward': 0,
                'unassigned': 0,
                'multi_wards': 0
            },
            'ward_manager': {
                'total': 0,
                'per_ward': 0,
                'unassigned': 0,
                'multi_wards': 0
            },
            'senior_manager': {
                'total': 0,
                'per_ward': 0,
                'unassigned': 0,
                'multi_wards': 0
            },
            'doctor': {
                'total': 0,
                'per_ward': 0,
                'unassigned': 0,
                'multi_wards': 0
            },
            'kiosk': {
                'total': 0,
                'per_ward': 0,
                'unassigned': 0,
                'multi_wards': 0
            },
            'admin': {
                'total': 0,
                'per_ward': 0,
                'unassigned': 0,
                'multi_wards': 0
            }
        }
        gen = UsersGenerator(basic_schema)
        self.assertEqual(gen.users_schema, basic_schema,
                         'Incorrect User Schema stored')

    def test_bed_number_method(self):
        """
        Test that the bed number generator works
        """
        gen = UsersGenerator({})
        bed_number_gen = gen.get_beds_number_generator(2)
        bed_number_first = bed_number_gen.next()
        bed_number_last = bed_number_gen.next()
        self.assertEqual(bed_number_first, 1, 'Incorrect first generator call')
        self.assertEqual(bed_number_last, 2, 'Incorrect last generator call')
