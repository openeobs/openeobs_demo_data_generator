# pylint: disable=R0201
# pylint: disable=R0915
# pylint: disable=R0914
"""
Generate users, based on locations created and wards assignment schema.
"""
from faker import Factory
from faker.providers.person.en import Provider
from xml.etree.ElementTree import Element, SubElement, Comment


class UsersXMLGenerator(object):

    def __init__(self, users_schema):
        """
        Initialise the users XML generator, declaring variables and generators.

        Particular attention must be payed to the ``users_schema`` parameter,
        since it must match the following specification:
        - every KEY is named after a specific user role in the system
          (e.g. 'hca', 'nurse', and so forth)
        - every corresponding VALUE must be a dictionary itself,
          whose couple key-value must be as following:
              key: 'total'
              value: number of users (for a specific role) present in the POS
              value type: integer

              key: 'per_ward'
              value: number of users (for a specific role) present in each ward
              value type: integer

              key: 'unassigned'
              value: number of users (for a specific role) not assigned to any
                     ward
              type: integer

              key: 'multi_wards'
              value: structure listing wards code, describing exactly
                     which wards each user (for a specific role) is assigned to
                     (this value can also accept the literal string 'all'
                     to briefly list all the wards present in the POS).
              value type: tuple of tuples (or string)

        :param users_schema: complete schema of users' assignment to wards
        :type users_schema: dict (see the docstring for further details)
        """
        self.users_schema = users_schema

        # Create root element
        self.class_root = Element('openerp')
        # Create data inside root element
        self.class_data = SubElement(self.class_root, 'data')

        self.data_generator = Factory.create()

        # Initialise additional user related data
        #
        # timezones
        self.timezone = 'Europe/London'
        # groups
        self.groups = {
            'hca': 'group_nhc_hca',
            'nurse': 'group_nhc_nurse',
            'ward_manager': 'group_nhc_ward_manager',
            'senior_manager': 'group_nhc_senior_manager',
            'doctor': 'group_nhc_doctor',
            'kiosk': 'group_nhc_kiosk',
            'admin': 'group_nhc_admin'
        }
        # roles (a.k.a. categories)
        self.categories = {
            'hca': 'role_nhc_hca',
            'nurse': 'role_nhc_nurse',
            'ward_manager': 'role_nhc_ward_manager',
            'senior_manager': 'role_nhc_senior_manager',
            'doctor': 'role_nhc_doctor',
            'kiosk': 'role_nhc_kiosk',
            'admin': 'role_nhc_admin'
        }
        self.assignable_to_ward = (
            'ward_manager',
            'doctor',
            'kiosk',
        )
        self.assignable_to_bed = (
            'hca',
            'nurse',
        )
        # First name generators, once per role.
        # Each of them returns only names starting by the initial letter
        # of the role denomination.
        self.names_generators = {
            'hca': (n for n in Provider.first_names
                    if n.lower().startswith('h')),
            'nurse': (n for n in Provider.first_names
                      if n.lower().startswith('n')),
            'ward_manager': (n for n in Provider.first_names
                             if n.lower().startswith('w')),
            'senior_manager': (n for n in Provider.first_names
                               if n.lower().startswith('s')),
            'doctor': (n for n in Provider.first_names
                       if n.lower().startswith('d')),
            'kiosk': (n for n in Provider.first_names
                      if n.lower().startswith('k')),
            'admin': (n for n in Provider.first_names
                      if n.lower().startswith('o'))
        }

    def get_beds_number_generator(self, beds_number):
        """Simple number generator."""
        for i in xrange(1, beds_number+1):
            yield i

    def build_user_data(self, xml_parent, role, first_name_generator, groups,
                        category, locations):
        """
        Extend the XML tree with elements defining a single user data.

        It doesn't return anything because modify the XML tree in place.

        :param xml_parent: XML element to append the user data tree to
        :param role: role of the user in the POS (e.g. 'hca', 'nurse', etc.)
        :type role: str
        :param first_name_generator: generator of name for a specific role
        :type first_name_generator: Python generator
        :param groups: group(s) the user belongs to
        :type groups: str
        :param category: role(s) the user belongs to
        :type category: str
        :param locations: location(s) assigned to the user
        :type locations: str
        """
        first_name = next(first_name_generator)
        last_name = self.data_generator.last_name()
        record = SubElement(xml_parent, 'record',
                            {'model': 'res.users',
                             'id': 'nhc_def_conf_{0}_{1}_user'.format(
                                 role, first_name.lower())})
        # Create user name field
        name_field = SubElement(record, 'field', {'name': 'name'})
        name_field.text = '{0} {1}'.format(first_name, last_name)
        # Create login field
        login_field = SubElement(record, 'field', {'name': 'login'})
        login_field.text = first_name.lower()
        # Create password field
        password_field = SubElement(record, 'field',
                                    {'name': 'password'})
        password_field.text = first_name.lower()
        # Create timezone field
        timezone_field = SubElement(record, 'field', {'name': 'tz'})
        timezone_field.text = self.timezone
        # Create groups field
        SubElement(record, 'field',
                   {'name': 'groups_id', 'eval': groups})
        # Create roles field
        SubElement(record, 'field',
                   {'name': 'category_id', 'eval': category})
        # Create location field
        SubElement(record, 'field',
                   {'name': 'location_ids', 'eval': locations})
        # Create pos field
        SubElement(record, 'field',
                   {'name': 'pos_id', 'ref': 'nhc_def_conf_pos_hospital'})

    def generate_adt_user(self):
        record = SubElement(self.class_data, 'record',
                            {'model': 'res.users',
                             'id': 'nhc_def_conf_adt_user'})
        name_field = SubElement(record, 'field', {'name': 'name'})
        name_field.text = 'GUH-ADT'

        login_field = SubElement(record, 'field', {'name': 'login'})
        login_field.text = 'adt'

        password_field = SubElement(record, 'field', {'name': 'password'})
        password_field.text = 'adt'

        SubElement(record, 'field',
                   {'name': 'groups_id',
                    'eval': "[(4, ref('nh_clinical.group_nhc_admin'))]"})

        SubElement(record, 'field',
                   {'name': 'category_id',
                    'eval': "[(4, ref('nh_clinical.role_nhc_admin'))]"})

        SubElement(record, 'field',
                   {'name': 'pos_id', 'ref': 'nhc_def_conf_pos_hospital'})

    def generate_users_per_ward(self, ward, beds_per_ward):
        """Create users assigned to wards or beds."""
        # Create root element
        root = Element('openerp')
        # Create data inside root element
        data = SubElement(root, 'data')

        for role, schema in self.users_schema.iteritems():
            # Initialise some variable to generate data for the current ward
            users_per_ward = schema.get('per_ward')
            if users_per_ward:
                groups_id = "[(4, ref('nh_clinical.{0}'))]".format(
                    self.groups[role])
                category_id = "[(4, ref('nh_clinical.{0}'))]".format(
                    self.categories[role])

                first_name_generator = self.names_generators.get(role)

                beds_per_user = beds_per_ward / users_per_ward

                # Initialise the generator for every users' role,
                # so it will supply sequential numbers coherently to all users.
                beds_number_generator = self.get_beds_number_generator(
                    beds_per_ward)

                # Add a comment to divide XML in sections by role
                users_role_comment = Comment(' Ward {0}: {1} '.format(
                    ward.upper(), role))
                data.append(users_role_comment)

                # Create user assigned to a specific ward (or beds).
                for _ in xrange(users_per_ward):
                    if role in self.assignable_to_ward:
                        location_ids = "[[6, False, " \
                                       "[ref('nhc_def_conf_location_w{}')]" \
                                       "]]".format(ward)
                    elif role in self.assignable_to_bed:
                        # Retrieve sequential numbers
                        # from the beds number generator,
                        # only for a very limited number of times
                        # (equal to number of beds per user).
                        #
                        # Use these sequential numbers
                        # to format strings about locations.
                        bed_list = ','.join(
                            ["ref('nhc_def_conf_location_w{}_b{}')".format(
                                ward, next(beds_number_generator))
                             for _ in xrange(beds_per_user)]
                        )
                        location_ids = "[[6, False, [{0}]]]".format(bed_list)
                    else:
                        location_ids = "[[6, False, []]]"
                    self.build_user_data(data, role, first_name_generator,
                                         groups_id, category_id, location_ids)
        return root

    def generate_users_not_assigned(self):
        """Create users not assigned to any ward."""
        for role, schema in self.users_schema.iteritems():
            # Initialise some variable to generate users data
            unassigned = schema.get('unassigned')
            if unassigned:
                groups_id = "[(4, ref('nh_clinical.{0}'))]".format(
                    self.groups[role])
                category_id = "[(4, ref('nh_clinical.{0}'))]".format(
                    self.categories[role])
                first_name_generator = self.names_generators.get(role)
                location_ids = "[[6, False, []]]"

                # Add a comment to divide XML in sections by role
                users_role_comment = Comment(' {0} '.format(role))
                self.class_data.append(users_role_comment)

                for _ in xrange(unassigned):
                    self.build_user_data(self.class_data, role,
                                         first_name_generator, groups_id,
                                         category_id, location_ids)

    def generate_multi_wards_users(self, wards_list):
        """
        Create users assigned to more than one ward
        (e.g. Senior manager, eObs admin)
        """
        for role, schema in self.users_schema.iteritems():
            # Initialise some variable to generate users data
            multi_wards = schema.get('multi_wards')
            total_users = schema.get('total')
            if multi_wards and total_users:
                groups_id = "[(4, ref('nh_clinical.{0}'))]".format(
                    self.groups[role])
                category_id = "[(4, ref('nh_clinical.{0}'))]".format(
                    self.categories[role])

                first_name_generator = self.names_generators.get(role)

                # Add a comment to divide XML in sections by role
                users_role_comment = Comment(' {0} '.format(role))
                self.class_data.append(users_role_comment)

                if multi_wards == 'all':
                    wards_location = ','.join(
                        ["ref('nhc_def_conf_location_w{}')".format(w)
                         for w in wards_list]
                    )
                    location_ids = "[[6, False, [{0}]]]".format(wards_location)
                    for _ in xrange(total_users):
                        self.build_user_data(self.class_data, role,
                                             first_name_generator, groups_id,
                                             category_id, location_ids)
                elif len(multi_wards) == total_users:
                    for wards in multi_wards:
                        wards_location = ','.join(
                            ["ref('nhc_def_conf_location_w{}')".format(w)
                             for w in wards]
                        )
                        location_ids = "[[6, False, [{0}]]]".format(
                            wards_location)
                        self.build_user_data(self.class_data, role,
                                             first_name_generator, groups_id,
                                             category_id, location_ids)
