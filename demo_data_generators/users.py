from faker import Factory
from faker.providers.person.en import Provider
from xml.etree.ElementTree import (Element, SubElement, dump, Comment,
                                   ElementTree)


class UsersXMLGenerator(object):

    def __init__(self, users_dictionary):
        """
        Initialise variables and generators used for users' data generation.

        :param users_dictionary: instruction to create an XML tree
        describing the right number and type of users for each role.

        This dictionary MUST have the following structure:
            {
                'hca': (total, assigned, unassigned),
                'nurse': (total, assigned, unassigned),
                'ward_manager': (total, assigned, unassigned),
                'doctor': (total, assigned, unassigned),
                'kiosk': (total, assigned, unassigned),
            }
        each element in the dictionary describes a specific role, where:
            - the KEYS must match the names of roles in the eObs system,
            - the VALUES must be tuples of 3 integers:
                (
                    number of total users (sum up from all the wards),
                    number of users assigned to bed(s) or ward locations,
                    number of users unassigned to any bed(s) or ward locations,
                )

        :type users_dictionary: dict
        """
        self.users_dictionary = users_dictionary

        self.data_generator = Factory.create()

        # Timezones
        self.timezone = 'Europe/London'

        # Groups
        self.groups = {
            'kiosk': 'group_nhc_kiosk',
            'doctor': 'group_nhc_doctor',
            'ward_manager': 'group_nhc_ward_manager',
            'nurse': 'group_nhc_nurse',
            'hca': 'group_nhc_hca'
        }

        # Roles (a.k.a. categories)
        self.categories = {
            'kiosk': 'role_nhc_kiosk',
            'doctor': 'role_nhc_doctor',
            'ward_manager': 'role_nhc_ward_manager',
            'nurse': 'role_nhc_nurse',
            'hca': 'role_nhc_hca'
        }

        # Pos
        self.pos = 'nhc_def_conf_pos_hospital'

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
            'doctor': (n for n in Provider.first_names
                       if n.lower().startswith('d')),
            'kiosk': (n for n in Provider.first_names
                      if n.lower().startswith('k'))
        }

    def indent(self, elem, level=0):
        """
        Pretty format an XML tree.

        It doesn't return anything, because it changes the XML tree in place.
        """
        i = '\n' + level * '  '
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def get_beds_number_generator(self, beds_number):
        for i in xrange(1, beds_number+1):
            yield i

    def generate_users(self, ward, beds_number, xml_file=None):
        """
        Generate an XML structure containing data for all the users,
        according to the instructions found in the class' users dictionary.

        :param ward: name of the ward (usually a single-letter code, e.g. 'a')
        :type ward: str
        :param beds_number: number of beds in the ward
        :type beds_number: int
        :param xml_file: path to an existing file to write the XML tree into
        :type xml_file: str
        """
        # Create root element
        root = Element('openerp')
        # Create data inside root element
        data = SubElement(root, 'data')

        for role, users_number in self.users_dictionary.iteritems():
            # Initialise some variable to generate data for the current ward
            total_users, users_per_ward, unassigned = users_number
            beds_per_user = beds_number / users_per_ward

            # Initialise the generator for every users' role,
            # thus it will supply sequential numbers coherently to all users.
            beds_number_generator = self.get_beds_number_generator(beds_number)
            groups_id = "[(4, ref('nh_clinical.{0}'))]".format(
                self.groups[role])
            category_id = "[(4, ref('nh_clinical.{0}'))]".format(
                self.categories[role])
            first_name_generator = self.names_generators[role]

            # Add a comment to divide XML in sections by role
            users_role_comment = Comment(' Ward {0}: {1} '.format(ward.upper(),
                                                                  role))
            data.append(users_role_comment)

            # Create user assigned to a specific ward and beds.
            # Every loop of the cycle, a different user is generated.
            for _ in xrange(users_per_ward):
                if role in ['nurse_in_charge', 'doctor', 'kiosk']:
                    location_ids = "[[6, False, " \
                                   "[ref('nhc_def_conf_location_w{}')]" \
                                   "]]".format(ward)
                elif role in ['hca', 'nurse']:
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

                first_name = next(first_name_generator)
                last_name = self.data_generator.last_name()
                record = SubElement(data, 'record',
                                    {'model': 'res.users',
                                     'id': 'nhc_def_conf_{0}_{1}_user'.format(
                                         role, first_name.lower())
                                     })
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
                           {'name': 'groups_id', 'eval': groups_id})
                # Create roles field
                SubElement(record, 'field',
                           {'name': 'category_id', 'eval': category_id})
                # Create location field
                SubElement(record, 'field',
                           {'name': 'location_ids', 'eval': location_ids})
                # Create pos field
                SubElement(record, 'field',
                           {'name': 'pos_id', 'ref': self.pos})

            # Create user not assigned to any ward
            for _ in xrange(unassigned):
                first_name = next(first_name_generator)
                last_name = self.data_generator.last_name()
                record = SubElement(data, 'record',
                                    {'model': 'res.users',
                                     'id': 'nhc_def_conf_{0}_{1}_user'.format(
                                         role, first_name.lower())
                                     })
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
                           {'name': 'groups_id', 'eval': groups_id})
                # Create roles field
                SubElement(record, 'field',
                           {'name': 'category_id', 'eval': category_id})
                # Create location field
                SubElement(record, 'field',
                           {'name': 'location_ids',
                            'eval': '[[6, False, []]]'})
                # Create pos field
                SubElement(record, 'field',
                           {'name': 'pos_id', 'ref': self.pos})

        # Pretty format the XML file
        self.indent(root)

        if not xml_file:
            # Print on system standard output
            dump(root)
        else:
            # Write to XML file
            xml_tree = ElementTree(root)
            xml_tree.write(xml_file)

"""
# Start the users generation !!!
wards_list = ['a', 'b', 'c', 'd', 'e']
beds_per_ward = 30
users_dictionary = {
    'hca': (55, 10, 5),
    'nurse': (55, 10, 5),
    'ward_manager': (6, 1, 1),
    'doctor': (24, 4, 1),
    'kiosk': (5, 1, 0),
}
data_folder = os.path.dirname(__file__)
users_generator = UsersXMLGenerator(users_dictionary)
for w in wards_list:
    #ward_folder = 'ward_{}'.format(w)
    #xml_folder = os.path.join(data_folder, ward_folder)
    #xml_file = os.path.join(xml_folder, 'demo_users.xml')
    users_generator.generate_users(
        w, beds_per_ward, os.path.join(data_folder,
                                       'ward_{}_users.xml'.format(w))
    )
"""
