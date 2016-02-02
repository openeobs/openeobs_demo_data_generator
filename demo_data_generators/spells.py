"""Generates spells"""
from xml.etree.ElementTree import Element, SubElement, Comment
import re


class SpellsGenerator(object):
    """Generates spells"""
    def __init__(self, patients, offsets):

        # Create root element
        self.root = Element('openerp')

        # Create data inside root element
        self.data = SubElement(self.root, 'data', {'noupdate': '1'})

        # Read the patient XML file
        patient_data = patients.data
        self.demo_patients = patient_data.findall('record')

        # List of time periods to randomly offset admissions
        self.offsets = offsets
        self.admit_date_eval_string = '(datetime.now() + timedelta({0}))' \
                                      '.strftime(\'%Y-%m-%d %H:%M:%S\')'

        # Regex to use to get the ID for a patient from id attribute on record
        patient_id_regex_string = r'nhc_demo_patient_(\d+)'
        self.patient_id_regex = re.compile(patient_id_regex_string)

        # Generate the patient admissions
        self.admit_patients()

    def generate_spell_data(self, patient_id, patient, admit_offset):
        """Generate Spell data"""
        self.data.append(
            Comment('Spell data for patient {0}'.format(patient_id))
        )
        self.create_activity_spell_record(patient_id, patient,
                                          admit_offset)
        self.create_spell_record(patient_id, patient, admit_offset)
        self.update_activity_spell(patient_id)

    def admit_patients(self):
        """
        Read the patients in the document and admit them to the locations they
        are in
        :return:
        """
        i = 0
        for patient in self.demo_patients:
            patient_id_match = re.match(self.patient_id_regex,
                                        patient.attrib['id'])
            patient_id = patient_id_match.groups()[0]

            self.generate_spell_data(patient_id, patient, self.offsets[i])
            i += 1

    def create_activity_spell_record(self, patient_id, patient, admit_offset):
        """Creates activity spell record"""

        # Create nh.activity ADT admission record with id
        activity_admit_record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.activity',
                'id': 'nhc_activity_demo_spell_{0}'.format(patient_id)
            }
        )

        state_field = SubElement(activity_admit_record, 'field',
                                 {'name': 'state'})
        state_field.text = 'started'

        # Create patient_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'patient_id',
                'ref': 'nhc_demo_patient_{0}'.format(patient_id)
            }
        )

        # Create activity data model
        activity_admit_model = SubElement(activity_admit_record,
                                          'field',
                                          {'name': 'data_model'})
        activity_admit_model.text = 'nh.clinical.spell'

        # Create parent_id reference
        location = patient.find('field[@name=\'current_location_id\']')\
            .attrib['ref']
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'location_id',
                'ref': location
            }
        )

        # Create activity date terminated
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'date_started',
                'eval': self.admit_date_eval_string.format(admit_offset)
            }
        )

    def create_spell_record(self, patient_id, patient, admit_offset):
        """Creates spell record"""

        # Create nh.clinical.adt.patient.admit record with id & data
        activity_admit_record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.clinical.spell',
                'id': 'nhc_demo_spell_{0}'.format(patient_id)
            }
        )

        # Create activity_id reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'activity_id',
                'ref': 'nhc_activity_demo_spell_{0}'.format(patient_id)
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
                'name': 'location_id',
                'ref': location
            }
        )

        # Create pos / hospital reference
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'pos_id',
                'ref': 'nh_clinical.nhc_location_default_pos'
            }
        )

        # Create code model
        admit_code = SubElement(activity_admit_record,
                                'field',
                                {'name': 'code'})
        admit_code.text = 'DEMO{0}'.format(patient_id.zfill(4))

        # Create activity date started
        SubElement(
            activity_admit_record,
            'field',
            {
                'name': 'start_date',
                'eval': self.admit_date_eval_string.format(admit_offset)
            }
        )

    def update_activity_spell(self, patient_id):
        """Update activity spell"""

        # Create nh.clinical.adt.patient.admit record with id & data
        update_activity_admit_record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.activity',
                'id': 'nhc_activity_demo_spell_{0}'.format(patient_id)
            }
        )

        # Create activity ref
        eval_string = '\'nh.clinical.spell,\' + ' \
                      'str(ref(\'nhc_demo_spell_{0}\'))'
        SubElement(
            update_activity_admit_record,
            'field',
            {
                'name': 'data_ref',
                'eval': eval_string.format(patient_id)
            }
        )

# wards = ['a']
# for ward in wards:
#     Generate_Spell_Data(ward)
