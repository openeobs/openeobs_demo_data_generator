from xml.etree.ElementTree import dump
from demo_data_generators.patients import PatientsGenerator
from demo_data_generators.spells import SpellsGenerator
from demo_data_generators.admissions import AdmissionsGenerator
from demo_data_generators.placements import PlacementsGenerator
import re


class DemoDataCoordinator(object):

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
            self.indent(patients)
            self.indent(spells)
            self.indent(admissions)
            self.indent(placements)

            with open('ward_{0}/demo_patients.xml'.format(ward), 'wb') as axml:
                axml.write(dump(patients.root))
            with open('ward_{0}/demo_spells.xml'.format(ward), 'wb') as bxml:
                bxml.write(dump(spells.root))
            with open('ward_{0}/demo_admissions.xml'.format(ward), 'wb') as \
                    cxml:
                cxml.write(dump(admissions.root))
            with open('ward_{0}/demo_placements.xml'.format(ward), 'wb') as \
                    dxml:
                dxml.write(dump(placements.root))

    def indent(self, elem, level=0):
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
