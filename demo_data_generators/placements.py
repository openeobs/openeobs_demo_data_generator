# pylint: disable=C0103
"""Generates placements"""
from xml.etree.ElementTree import Element, SubElement, Comment
import random
import re


class PlacementsGenerator(object):
    """Generates placements"""
    def __init__(self, patients):

        # Create root element
        self.root = Element('openerp')

        # Create data inside root element
        self.data = SubElement(self.root, 'data', {'noupdate': '1'})

        # Read the patient XML file
        patient_data = patients.data
        self.demo_patients = patient_data.findall('record')

        # List of time periods to randomly offset admissions
        self.admit_offset_list = ['-1', '-2']
        self.admit_date_eval_string = '(datetime.now() + timedelta({0}))' \
                                      '.strftime(\'%Y-%m-%d %H:%M:%S\')'

        # Regex to use to get the ID for a patient from id attribute on record
        patient_id_regex_string = r'nhc_demo_patient_(\d+)'
        ward_regex_string = r'(nhc_def_conf_location_w\w)'
        self.patient_id_regex = re.compile(patient_id_regex_string)
        self.ward_regex = re.compile(ward_regex_string)

        # Generate the patient admissions
        self.admit_patients()

    def remove_bed(self, bed_string):
        """Removes a bed"""
        ward_location = re.match(self.ward_regex, bed_string)
        return ward_location.groups()[0]

    def generate_placement_data(self, patient_id, patient, admit_offset):
        """Generate placement data"""
        self.data.append(
            Comment(
                'Placement data for patient {0}'.format(patient_id)
            )
        )
        self.create_activity_placement_record(patient_id, patient,
                                              admit_offset)
        self.create_placement_record(patient_id, patient)
        self.update_activity_placement(patient_id)

    def generate_placement_movement_data(self, patient_id, patient,
                                         admit_offset):
        """Generate Spell Movement Data"""
        self.data.append(
            Comment('Spell movement for patient {0}'.format(patient_id))
        )
        self.create_activity_placement_movement_record(patient_id, patient,
                                                       admit_offset)
        self.create_placement_movement_record(patient_id, patient)
        self.update_activity_placement_movement(patient_id)

    def admit_patients(self):
        """
        Read the patients in the document and admit them to the locations they
        are in
        :return:
        """
        for patient in self.demo_patients:
            patient_id_match = re.match(self.patient_id_regex,
                                        patient.attrib['id'])
            patient_id = patient_id_match.groups()[0]
            admit_offset = random.choice(self.admit_offset_list)
            # Generate placement data
            location_el = patient.find('field[@name=\'current_location_id\']')
            location = location_el.attrib['ref']
            if '_b' in location[-6:]:
                self.generate_placement_data(patient_id, patient, admit_offset)
                self.generate_placement_movement_data(patient_id, patient,
                                                      admit_offset)

    def create_activity_placement_record(self, patient_id, patient,
                                         admit_offset):
        """Create activity placement record"""

        # Create nh.activity ADT admission record with id
        activity_admit_record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.activity',
                'id': 'nhc_activity_demo_placement_{0}'.format(patient_id)
            }
        )

        # Create patient_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'patient_id',
                'ref': 'nhc_demo_patient_{0}'.format(patient_id)
            }
        )

        # Create creator_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'creator_id',
                'ref': 'nhc_activity_demo_admission_{0}'.format(patient_id)
            }
        )

        # Create parent_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'parent_id',
                'ref': 'nhc_activity_demo_spell_{0}'.format(patient_id)
            }
        )

        # Create spell_activity_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'spell_activity_id',
                'ref': 'nhc_activity_demo_spell_{0}'.format(patient_id)
            }
        )

        # Create activity state
        activity_admit_state = SubElement(activity_admit_record,
                                          'field',
                                          {'name': 'state'})
        activity_admit_state.text = 'completed'

        # Create activity data model
        activity_admit_model = SubElement(activity_admit_record,
                                          'field',
                                          {'name': 'data_model'})
        activity_admit_model.text = 'nh.clinical.patient.placement'

        # Create parent_id reference
        location = patient.find('field[@name=\'current_location_id\']')\
            .attrib['ref']
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'location_id',
                'ref': self.remove_bed(location)
            }
        )

        # Create activity date terminated
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'date_terminated',
                'eval': self.admit_date_eval_string.format(admit_offset)
            }
        )

    def create_placement_record(self, patient_id, patient):
        """Create placement record"""

        # Create nh.clinical.adt.patient.admit record with id & data
        activity_admit_record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.clinical.patient.placement',
                'id': 'nhc_demo_placement_{0}'.format(patient_id)
            }
        )

        # Create activity_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'activity_id',
                'ref': 'nhc_activity_demo_placement_{0}'.format(patient_id)
            }
        )

        # Create patient_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'patient_id',
                'ref': 'nhc_demo_patient_{0}'.format(patient_id)
            }
        )

        # Create parent_id reference
        location = patient.find('field[@name=\'current_location_id\']')\
            .attrib['ref']
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'suggested_location_id',
                'ref': self.remove_bed(location)
            }
        )

        # Create pos / hospital reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'location_id',
                'ref': location
            }
        )

    def update_activity_placement(self, patient_id):
        """Update activity placement"""

        # Create nh.clinical.adt.patient.admit record with id & data
        update_activity_admit_record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.activity',
                'id': 'nhc_activity_demo_placement_{0}'.format(patient_id)
            }
        )

        # Create activity ref
        eval_string = '\'nh.clinical.patient.placement,\' + ' \
                      'str(ref(\'nhc_demo_placement_{0}\'))'
        SubElement(
            update_activity_admit_record,
            'field',
            {
                'name': 'data_ref',
                'eval': eval_string.format(patient_id)
            }
        )

    def create_activity_placement_movement_record(self, patient_id, patient,
                                                  admit_offset):
        """Create activity placement movement record"""
        activity_admit_record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.activity',
                'id': 'nhc_activity_demo_placement_move_{0}'.format(patient_id)
            }
        )

        # Create patient_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'patient_id',
                'ref': 'nhc_demo_patient_{0}'.format(patient_id)
            }
        )

        # Create creator_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'creator_id',
                'ref': 'nhc_activity_demo_placement_{0}'.format(patient_id)
            }
        )

        # Create parent_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'parent_id',
                'ref': 'nhc_activity_demo_spell_{0}'.format(patient_id)
            }
        )

        # Create spell_activity_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'spell_activity_id',
                'ref': 'nhc_activity_demo_spell_{0}'.format(patient_id)
            }
        )

        # Create state
        state_field = SubElement(activity_admit_record, 'field',
                                 {'name': 'state'})
        state_field.text = 'completed'

        # Create activity data model
        activity_admit_model = SubElement(activity_admit_record,
                                          'field',
                                          {'name': 'data_model'})
        activity_admit_model.text = 'nh.clinical.patient.move'

        # Create parent_id reference
        location = patient.find('field[@name=\'current_location_id\']')\
            .attrib['ref']
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'location_id',
                'ref': self.remove_bed(location)
            }
        )

        # Create activity date terminated
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'date_terminated',
                'eval': self.admit_date_eval_string.format(admit_offset)
            }
        )

    def create_placement_movement_record(self, patient_id, patient):
        """Create placement movement record"""
        activity_admit_record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.clinical.patient.move',
                'id': 'nhc_demo_placement_move_{0}'.format(patient_id)
            }
        )

        # Create activity_id reference
        activity_id_ref = 'nhc_activity_demo_placement_move_{0}'
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'activity_id',
                'ref': activity_id_ref.format(patient_id)
            }
        )

        # Create patient_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'patient_id',
                'ref': 'nhc_demo_patient_{0}'.format(patient_id)
            }
        )

        # Create parent_id reference
        location = patient.find('field[@name=\'current_location_id\']')\
            .attrib['ref']
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'from_location_id',
                'ref': self.remove_bed(location)
            }
        )
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'location_id',
                'ref': location
            }
        )

    def update_activity_placement_movement(self, patient_id):
        """Update activity placement movement"""

        # Create nh.clinical.adt.patient.admit record with id & data
        update_activity_admit_record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.activity',
                'id': 'nhc_activity_demo_placement_move_{0}'.format(patient_id)
            }
        )

        # Create activity ref
        eval_string = '\'nh.clinical.patient.move,\' + ' \
                      'str(ref(\'nhc_demo_placement_move_{0}\'))'
        SubElement(
            update_activity_admit_record,
            'field',
            {
                'name': 'data_ref',
                'eval': eval_string.format(patient_id)
            }
        )
