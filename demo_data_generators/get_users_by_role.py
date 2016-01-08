"""
Simple script to scan a directory structure, searching into XML files
for open-eObs demo data, and print out a user's name for each specific role.
"""
import os
from pprint import pprint
from xml.etree.ElementTree import ElementTree


def get_first_user_per_role(users_per_role, element):
    """
    Update a dictionary (passed as argument) with a user's complete name
    for each role list as that dictionary's key.

    :param users_per_role: dictionary listing the desired roles
    :type users_per_role: dict
    :param element: an XML element to search into
    """
    for role in users_per_role:
        for user in element.findall('record'):
            if role in user.attrib['id']:
                for field in user.findall('field'):
                    if field.get('name') == 'name':
                        users_per_role[role] = field.text
                break
    return users_per_role


def main():
    # Some hardcoded variables needed to find and properly parse the XML files
    wards_list = ['a', 'b', 'c', 'd', 'e']
    data_folder = os.path.join(os.path.dirname(__file__), 'DATA')
    role_assigned_to_ward = {
        'nurse': None,
        'hca': None,
        'ward_manager': None,
        'doctor': None
    }

    # Search into an XML file (and print the result) for each ward's folder
    for ward in wards_list:
        ward_folder = os.path.join(data_folder, 'ward_{0}'.format(ward))
        xml_file = os.path.join(ward_folder, 'demo_users.xml')
        tree = ElementTree(file=xml_file)
        data = tree.getroot().find('data')
        roles_dict = dict(role_assigned_to_ward)
        per_ward_output = get_first_user_per_role(roles_dict, data)
        print('WARD {0}:'.format(ward.upper()))
        pprint(per_ward_output)

    # Search into the generic XML file for users not assigned to any ward
    role_unassigned = {
        'admin': None,
        'nurse': None,
        'hca': None,
        'senior_manager': None,
        'ward_manager': None,
        'doctor': None
    }
    xml_file = os.path.join(data_folder, 'users.xml')
    tree = ElementTree(file=xml_file)
    data = tree.getroot().find('data')
    unassigned_roles_dict = dict(role_unassigned)
    unassigned_output = get_first_user_per_role(unassigned_roles_dict, data)
    print('USERS NOT ASSIGNED TO ANY WARD:')
    pprint(unassigned_output)

if __name__ == '__main__':
    main()
