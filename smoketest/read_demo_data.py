import erppeek
import unittest


def get_erppeek_client(server='http://localhost:8069', db='openerp',
                       user='admin', password='admin'):
    """
    Get a ERPPeek client for us to use, if one not available then close the
    function
    :param server: Server address (with XML-RPC port)
    :param db: Name of database
    :param user: Username to connect with
    :param password: Password for username connecting with
    :return: A erppeek.Client object we can use for XML-RPC calls
    """
    try:
        client = erppeek.Client(server, db=db, user=user, password=password,
                                verbose=False)
    except:
        raise RuntimeError(
            "Error connecting to {0} on {1} using credentials {2}:{3}".format(
                db, server, user, password
            )
        )
    return client


class UsersSmokeTest(unittest.TestCase):

    SERVER = 'http://localhost:8069'
    DATABASE = 'nhclinical'
    USER = 'admin'
    PASSWORD = 'admin'

    def setUp(self):
        self.client = get_erppeek_client(server=self.SERVER,
                                    db=self.DATABASE, user=self.USER,
                                    password=self.PASSWORD)

        self.hospital_pos = self.client.search('nh.clinical.location',
                                             [['code', '=', 'GUH']])
        self.hospital_search = self.client.search('nh.clinical.pos',
                                                  [
                                                      ['location_id',
                                                       'in',
                                                       self.hospital_pos]
                                                  ])[0]
        self.hospital = self.client.read('nh.clinical.pos',
                                         self.hospital_search,
                                         ['name'])['name']

        self.senior_ids = self.client.read('res.partner.category',
                                       [('name','=','Senior Manager')],
                                       'child_ids')
        self.senior_managers = len(self.senior_ids[0])

        self.wards = self.client.read('nh.clinical.location',
                                        [('usage', '=', 'ward')])
        self.ward_names = []
        for ward in self.wards:
              self.ward_names.append(ward['name'])

        self.patients = 0
        for ward in self.wards:
            self.patients += len(ward['patient_ids'])

        self.nurse_list = []
        for ward in self.wards:
            self.nurse_list.append(ward['assigned_nurse_ids'])

        self.doctor_list = []
        for ward in self.wards:
            self.doctor_list.append(ward['assigned_doctor_ids'])

        self.hca_list = []
        for ward in self.wards:
            self.hca_list.append(ward['related_hcas'])

        self.beds = self.client.read('nh.clinical.location', [('usage', '=', 'bed')])
        self.bed_total = []
        for ward in self.wards:
            self.bed_list = []
            for bed in self.beds:
               if ward['name'] in bed['full_name']:
                 self.bed_list.append(bed)
            self.bed_total.append(len(self.bed_list))

    def test_hospital_name(self):
        self.assertEqual(self.hospital, 'Greenfield University Hospital',
                         'Incorrect hospital name')

    def test_senior_managers(self):
        self.assertEqual(self.senior_managers, 3,
                         'Incorrect amount of managers')

    def test_wards(self):
        self.assertEqual(self.ward_names,
                         ['Ward A','Ward B','Ward C','Ward D','Ward E'],
                         'Incorrect ward names')

    def test_total_patients(self):
        self.assertEqual(self.patients, 200, 'Incorrect total of patients')

    def test_ward_patients(self):
        for ward in self.wards:
            self.assertEqual(len(ward['patient_ids']), 40,
                                 'Incorrect amount of patients in ward ' + ward['name'])

    def test_ward_nurses(self):
        for ward in self.wards:
            for list in self.nurse_list:
                self.assertEqual(len(list), 10, 'Incorrect number of nurses in ' + ward['name'])

    def test_ward_doctors(self):
        for list in self.doctor_list:
            self.assertEqual(len(list), 4, 'Incorrect number of doctors')

    def test_ward_hcas(self):
        for hca in self.hca_list:
            self.assertEqual(hca, 10, 'Incorrect number of hcas')

    def test_beds(self):
        for beds in self.bed_total:
            self.assertEqual(beds, 30, 'Incorrect number of beds')
