# pylint: disable=R0913
# pylint: disable=C0103
"""
Generate Ward and defined number of beds
"""
from xml.etree.ElementTree import Element, SubElement


class LocationsGenerator(object):
    """
    Generate Locations
    """

    def __init__(self, ward_name, beds_per_ward):

        # Create root element
        self.root = Element('openerp')

        # Create data inside root element
        self.data = SubElement(self.root, 'data', {'noupdate': '1'})

        self.generate_location(ward_name, 'Ward {0}'.format(ward_name.upper()),
                               'ward', False, ward_name, 0)
        self.generate_beds(beds_per_ward, ward_name)

    def generate_beds(self, number_of_beds, ward_name):
        """
        A function to create a bunch of patients for the XML document
        :param number_of_beds: The number of beds to generate
        :type number_of_beds: int
        :param ward_name: Name of the ward beds belong in
        :type ward_name: str
        """
        for item in xrange(0, number_of_beds):
            bed_id = item + 1
            self.generate_location('{0}_b{1}'.format(ward_name, bed_id),
                                   'Bed {0}'.format(bed_id), 'bed',
                                   'w{0}'.format(ward_name), ward_name, bed_id)

    def generate_location(self, rid, name, usage, parent, ward, bed_number,
                          context=None):
        """Generate a location"""
        # Create record with location data
        record = SubElement(
            self.data,
            'record',
            {
                'model': 'nh.clinical.location',
                'id': 'nhc_def_conf_location_w{0}'.format(rid)
            }
        )

        # create name field with fake data
        name_field = SubElement(record, 'field', {'name': 'name'})
        name_field.text = name

        # create code field with fake data
        code_field = SubElement(record, 'field', {'name': 'code'})
        if usage == 'ward':
            code_field.text = ward.upper()
        elif usage == 'bed':
            code_field.text = '{0}{1}'.format(ward.upper(), bed_number)
        else:
            code_field.text = rid.upper().replace('_', '')

        # create type field
        type_field = SubElement(record, 'field', {'name': 'type'})
        type_field.text = 'poc'

        # create usage field
        usage_field = SubElement(record, 'field', {'name': 'usage'})
        usage_field.text = usage

        # create a reference to parent location
        if parent:
            SubElement(record, 'field', {
                'name': 'parent_id',
                'ref': 'nhc_def_conf_location_{0}'.format(parent)
            })
        else:
            SubElement(record, 'field', {
                'name': 'parent_id',
                'ref': 'nh_clinical.nhc_location_default_hospital'
            })

        # create a reference to context
        if not context:
            context = "nh_eobs.nh_eobs_context"
        SubElement(record, 'field', {
            'name': 'context_ids',
            'eval': "[[6, False, [ref('{0}')]]]".format(context)
            })
