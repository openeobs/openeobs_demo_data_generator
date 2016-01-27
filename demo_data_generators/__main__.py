""" CLI foo for demo data generator
"""
import sys
import os
import argparse
import json
import yaml
import logging
from demo_data_generators.demo_data_coordinator import DemoDataCoordinator


_logger = logging.getLogger(__name__)

DEFAULT_USERS = '{"doctor": {"unassigned": 4, "total": 24, "per_ward": 4}, ' \
                '"admin": {"unassigned": 0, "multi_wards": "all", "total": 1' \
                ', "per_ward": 0}, "kiosk": {"unassigned": 0, "total": 5, ' \
                '"per_ward": 1}, "senior_manager": {"unassigned": 0, ' \
                '"multi_wards": [["a", "b", "c"], ["d", "e"], ' \
                '["a", "b", "c", "d", "e"]], "total": 3, "per_ward": 0}, ' \
                '"hca": {"unassigned": 5, "total": 55, "per_ward": 10}, ' \
                '"nurse": {"unassigned": 5, "total": 55, "per_ward": 10},' \
                ' "ward_manager": {"unassigned": 1, "total": 6, "per_ward": ' \
                '1}}'
try:
    with open('users_schema.yaml') as yaml_file:
        DEFAULT_USERS_YAML = yaml.load(yaml_file)
except IOError:
    _logger.debug("No YAML file named 'users_schema.yaml' can be found "
                  "for the users schema configuration.")
    DEFAULT_USERS_YAML = None

PARSER = argparse.ArgumentParser('Generate demo data for NH Clinical')
PARSER.add_argument('data_folder', type=str,
                    help='Folder in which to generate the data')
PARSER.add_argument('--wards', type=str,
                    help='CSV list of ward names',
                    default='a,b,c,d,e')
PARSER.add_argument('--beds', type=int,
                    help='Number of beds per ward',
                    default=30)
PARSER.add_argument('--patientsinbed', type=int,
                    help='Number of patients in a bed', default=28)
PARSER.add_argument('--patientsnotinbed', type=int,
                    help='Number of patients not in a bed', default=12)
PARSER.add_argument('--users', type=str,
                    help='JSON for user break down', default=DEFAULT_USERS)
PARSER.add_argument('--users-yaml', type=str, help='YAML for user break down',
                    dest='users_yaml', default=DEFAULT_USERS_YAML)


def main():
    """
    Parse the args and generate the demo data
    """
    args = PARSER.parse_args()
    data_folder = args.data_folder
    wards = args.wards
    beds_per_ward = args.beds
    bed_patient_per_ward = args.patientsinbed
    non_bed_patient_per_ward = args.patientsnotinbed
    users_schema = args.users
    users_schema_yaml = args.users_yaml

    if wards:
        wards = wards.replace(' ', '').split(',')
    if users_schema_yaml:
        users_schema = yaml.load(users_schema_yaml)
    elif users_schema:
        users_schema = json.loads(users_schema)
    if data_folder:
        data_folder = sanitise_data_folder(data_folder)

    DemoDataCoordinator(wards=wards,
                        beds_per_ward=beds_per_ward,
                        bed_patient_per_ward=bed_patient_per_ward,
                        non_bed_patient_per_ward=non_bed_patient_per_ward,
                        users_schema=users_schema,
                        data_folder=data_folder)


def sanitise_data_folder(folder_path):
    if '~' in folder_path:
        return os.path.expanduser(folder_path)
    if os.path.isabs(folder_path):
        return folder_path
    else:
        return os.path.abspath(folder_path)

if __name__ == '__main__':
    sys.exit(main())
