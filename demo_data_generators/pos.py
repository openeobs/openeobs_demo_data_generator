# pylint: disable=R0913
# pylint: disable=C0103
"""
Generate POS, Location lots and Hospital.
"""
from xml.etree.ElementTree import Element, SubElement


class POSGenerator(object):
    """
    Generate POS
    """

    def __init__(self):

        # Create root element
        self.root = Element('openerp')

        # Create data inside root element
        self.data = SubElement(self.root, 'data')

        self.generate_pos()
        self.generate_location_lots()
        self.generate_hospital()

    def generate_pos(self):
        """Create POS data as an XML tree."""
        record = SubElement(self.data, 'record',
                            {'model': 'nh.clinical.location',
                             'id': 'nh_clinical.nhc_location_default_hospital'})
        # Create name field
        name_field = SubElement(record, 'field', {'name': 'name'})
        name_field.text = 'Greenfield University Hospital'
        # Create code field
        code_field = SubElement(record, 'field', {'name': 'code'})
        code_field.text = 'GUH'
        # Create type field
        type_field = SubElement(record, 'field', {'name': 'type'})
        type_field.text = 'pos'
        # Create usage field
        usage_field = SubElement(record, 'field', {'name': 'usage'})
        usage_field.text = 'hospital'

    def generate_location_lots(self):
        """Create Location lots data as an XML tree."""
        # Create Admission Location lot
        record = SubElement(self.data, 'record',
                            {'model': 'nh.clinical.location',
                             'id': 'nhc_def_conf_location_lot_admission'})

        name_field = SubElement(record, 'field', {'name': 'name'})
        name_field.text = 'Admission Location'

        code_field = SubElement(record, 'field', {'name': 'code'})
        code_field.text = 'ADML-GUH'

        type_field = SubElement(record, 'field', {'name': 'type'})
        type_field.text = 'structural'

        usage_field = SubElement(record, 'field', {'name': 'usage'})
        usage_field.text = 'room'

        SubElement(record, 'field', {
            'name': 'parent_id',
            'ref': 'nh_clinical.nhc_location_default_hospital'})

        # Create Discharge Location lot
        record = SubElement(self.data, 'record',
                            {'model': 'nh.clinical.location',
                             'id': 'nhc_def_conf_location_lot_discharge'})

        name_field = SubElement(record, 'field', {'name': 'name'})
        name_field.text = 'Discharge Location'

        code_field = SubElement(record, 'field', {'name': 'code'})
        code_field.text = 'DISL-GUH'

        type_field = SubElement(record, 'field', {'name': 'type'})
        type_field.text = 'structural'

        usage_field = SubElement(record, 'field', {'name': 'usage'})
        usage_field.text = 'room'

        SubElement(record, 'field', {
            'name': 'parent_id',
            'ref': 'nh_clinical.nhc_location_default_hospital'})

    def generate_hospital(self):
        """Create Hospital data as an XML tree."""
        record = SubElement(self.data, 'record',
                            {'model': 'nh.clinical.pos',
                             'id': 'nh_clinical.nhc_location_default_pos'})

        name_field = SubElement(record, 'field', {'name': 'name'})
        name_field.text = 'Greenfield University Hospital'

        SubElement(record, 'field', {
            'name': 'location_id',
            'ref': 'nh_clinical.nhc_location_default_hospital'})

        SubElement(record, 'field', {'name': 'company_id',
                                     'ref': 'base.main_company'})

        SubElement(record, 'field',
                   {'name': 'lot_admission_id',
                    'ref': 'nhc_def_conf_location_lot_admission'})

        SubElement(record, 'field',
                   {'name': 'lot_discharge_id',
                    'ref': 'nhc_def_conf_location_lot_discharge'})
