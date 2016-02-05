# pylint: disable=R0913
# pylint: disable=C0103
"""
Creates POS and Hospital records.
"""
from base import Document


class POSGenerator(Document):
    """Creates a POS XML document."""
    def __init__(self):
        super(POSGenerator, self).__init__()
        self.create_pos_record()
        self.create_hospital_record()

    def create_pos_record(self):
        """Creates POS record."""
        record = self.record(
            {'model': 'nh.clinical.location',
             'id': 'nh_clinical.nhc_location_default_hospital'})
        record.field({'name': 'name',
                      'value': 'Greenfield University Hospital'})
        record.field({'name': 'code', 'value': 'GUH'})
        record.field({'name': 'type', 'value': 'pos'})
        record.field({'name': 'usage', 'value': 'hospital'})

    def create_hospital_record(self):
        """Creates Hospital record."""
        record = self.record({'model': 'nh.clinical.pos',
                              'id': 'nh_clinical.nhc_location_default_pos'})
        record.field({'name': 'name',
                      'value': 'Greenfield University Hospital'})
        record.field({'name': 'location_id',
                      'ref': 'nh_clinical.nhc_location_default_hospital'})
        record.field({'name': 'company_id', 'ref': 'base.main_company'})
