# pylint: disable=R0903
# pylint: disable=R0914
"""Coordinates demo data"""
from xml.etree.ElementTree import tostring
from demo_data_generators.patients import PatientsGenerator
from demo_data_generators.spells import SpellsGenerator
from demo_data_generators.admissions import AdmissionsGenerator
from demo_data_generators.placements import PlacementsGenerator
import re
import os


class DemoDataCoordinator(object):
    """Coordinates demo data"""
    def __init__(self, wards, bed_patient_per_ward, non_bed_patient_per_ward):

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

        for index, ward in enumerate(wards):
            patients = PatientsGenerator(
                (index * total_patients_per_ward) + patient_id_offset,
                bed_patient_per_ward,
                non_bed_patient_per_ward,
                ward
            )
            spells = SpellsGenerator(patients)
            admissions = AdmissionsGenerator(patients)
            placements = PlacementsGenerator(patients)
            # Pretty Print the XML file
            self.indent(patients.root)
            self.indent(spells.root)
            self.indent(admissions.root)
            self.indent(placements.root)

            if not os.path.isdir('ward_{0}'.format(ward)):
                os.mkdir('ward_{0}'.format(ward))
            with open('ward_{0}/demo_patients.xml'.format(ward), 'wb') as axml:
                axml.write(tostring(patients.root))
            with open('ward_{0}/demo_spells.xml'.format(ward), 'wb') as bxml:
                bxml.write(tostring(spells.root))
            with open('ward_{0}/demo_admissions.xml'.format(ward), 'wb') as \
                    cxml:
                cxml.write(tostring(admissions.root))
            with open('ward_{0}/demo_placements.xml'.format(ward), 'wb') as \
                    dxml:
                dxml.write(tostring(placements.root))

    def indent(self, elem, level=0):
        """Indents data"""
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
