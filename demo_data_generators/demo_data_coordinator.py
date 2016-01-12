# pylint: disable=R0903
# pylint: disable=R0914
"""Coordinates demo data"""
import re
import os

from xml.etree.ElementTree import ElementTree
from demo_data_generators.admissions import AdmissionsGenerator
from demo_data_generators.locations import LocationsGenerator
from demo_data_generators.patients import PatientsGenerator
from demo_data_generators.placements import PlacementsGenerator
from demo_data_generators.pos import POSGenerator
from demo_data_generators.spells import SpellsGenerator
from demo_data_generators.users import UsersGenerator
from demo_data_generators.ward_strategy import patients_factory, WardStrategy
from demo_data_generators.news import NewsGenerator


class DemoDataCoordinator(object):
    """Coordinate demo data generation."""
    def __init__(self, wards, beds_per_ward, bed_patient_per_ward,
                 non_bed_patient_per_ward, users_schema, data_folder):

        total_patients_per_ward = \
            bed_patient_per_ward + non_bed_patient_per_ward
        patient_id_offset = 1
        # wards = ['a', 'b', 'c', 'd', 'e']
        # bed_patients_per_ward = 28
        # non_bed_patients_per_ward = 12

        # List of time periods to randomly offset admissions
        self.admit_offset_list = ['-1', '-2']
        self.admit_date_eval_string = '(datetime.now() + timedelta({0}))' \
                                      '.strftime(\'%Y-%m-%d 00:00:00\')'

        # Regex to use to get the ID for a patient from id attribute on record
        patient_id_regex_string = r'nhc_demo_patient_(\d+)'
        self.patient_id_regex = re.compile(patient_id_regex_string)

        point_of_service = POSGenerator()
        self.indent(point_of_service.root)
        users_tree = ElementTree(point_of_service.root)
        users_tree.write(os.path.join(data_folder, 'pos.xml'))

        users_generator = UsersGenerator(users_schema)
        users_generator.generate_adt_user()
        users_generator.generate_multi_wards_users(wards)
        users_generator.generate_users_not_assigned()
        self.indent(users_generator.class_root)
        users_tree = ElementTree(users_generator.class_root)
        users_tree.write(os.path.join(data_folder, 'users.xml'))

        # Generate demo data for each ward,
        # with files named after different type of data,
        # grouped in one folder for each ward
        for index, ward in enumerate(wards):
            # Locations demo data
            locations = LocationsGenerator(ward, beds_per_ward)
            # Users demo data
            users_per_ward_root = users_generator.generate_users_per_ward(
                ward, beds_per_ward)
            # Patients demo data
            patients = PatientsGenerator(
                (index * total_patients_per_ward) + patient_id_offset,
                bed_patient_per_ward,
                non_bed_patient_per_ward,
                ward
            )
            # Spells demo data
            spells = SpellsGenerator(patients)
            # Admissions demo data
            admissions = AdmissionsGenerator(patients)
            # Placements demo data
            placements = PlacementsGenerator(patients)

            # set strategy parameters for ward
            news_patients = patients_factory(placements.root)
            risk_distribution = {'high': 1, 'medium': 2, 'low': 10, 'none': 15}
            partial_news_per_patient = 1
            # Generate ward strategy here
            ward_strategy = WardStrategy(
                news_patients, risk_distribution, partial_news_per_patient
            )

            # NEWS demo data
            news = NewsGenerator(ward_strategy)

            # Pretty format the XML trees
            self.indent(locations.root)
            self.indent(users_per_ward_root)
            self.indent(patients.root)
            self.indent(spells.root)
            self.indent(admissions.root)
            self.indent(placements.root)
            self.indent(news.root)

            # Actually write the XML files (creating them if needed)
            ward_folder = os.path.join(data_folder, 'ward_{0}'.format(ward))
            if not os.path.isdir(ward_folder):
                os.mkdir(ward_folder)

            locations_tree = ElementTree(locations.root)
            locations_tree.write(os.path.join(ward_folder,
                                              'demo_locations.xml'))

            users_per_ward_tree = ElementTree(users_per_ward_root)
            users_per_ward_tree.write(os.path.join(ward_folder,
                                                   'demo_users.xml'))

            patients_tree = ElementTree(patients.root)
            patients_tree.write(os.path.join(ward_folder, 'demo_patients.xml'))

            spells_tree = ElementTree(spells.root)
            spells_tree.write(os.path.join(ward_folder, 'demo_spells.xml'))

            admissions_tree = ElementTree(admissions.root)
            admissions_tree.write(os.path.join(ward_folder,
                                               'demo_admissions.xml'))

            placements_tree = ElementTree(placements.root)
            placements_tree.write(os.path.join(ward_folder,
                                               'demo_placements.xml'))
            news_tree = ElementTree(news.root)
            news_tree.write(os.path.join(ward_folder, 'demo_news.xml'))

    def indent(self, elem, level=0):
        """Indent data stored in an XML tree."""
        i = "\n" + level*"  "
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
