import erppeek
import unittest


def get_erppeek_client(server='http://localhost:8069', db='nhclinical',
                       user='adt', password='adt'):
    """
    Get a ERPPeek client for us to use, if one not available then close the
    function
    :param server: Server address (with XML-RPC port)
    :param db: Name of database
    :param user: Username to connect with
    :param password: Password for username connecting with
    :return: A erppeek.Client object we can use for XML-RPC calls
    """
    client = erppeek.Client(server, db=db, user=user, password=password,
                            verbose=False)
    return client


class MobileSmokeTest(unittest.TestCase):

    SERVER = 'http://localhost:8069'
    DATABASE = 'nhclinical'
    USER = 'nasir'
    PASSWORD = 'nasir'

    def setUp(self):
        self.client = get_erppeek_client(server=self.SERVER,
                                    db=self.DATABASE, user=self.USER,
                                    password=self.PASSWORD)
        self.api_pool = self.client.model('nh.eobs.api')

    def test_task_list(self):
        assigned_activities = self.api_pool.get_assigned_activities(
            activity_type='nh.clinical.patient.follow')
        self.assertTrue(len(assigned_activities) > 0)

    def test_patient_list_contains_following_notifications(self):
        self.api_pool.unassign_my_activities()
        follow_activities = self.api_pool.get_assigned_activities()
        self.assertTrue(len(follow_activities) > 0)

    def test_patient_list_contains_following_patients(self):
        patients = self.api_pool.get_patients([])
        self.assertEqual(patients, '')
        following_patients = self.api_pool.get_followed_patients()
        self.assertTrue(len(following_patients) > 0)

    def test_patient_follow(self):
        follow_pool = self.client.model('nh.clinical.patient.follow')
        followed_ids = follow_pool.search([])
        self.assertTrue(len(followed_ids) > 0)

    def test_there_are_follow_activities(self):
        activity_pool = self.client.model('nh.activity')
        activity_ids = activity_pool.search(
            [('data_model', '=', 'nh.clinical.patient.follow')])
        self.assertTrue(len(activity_ids) > 0)


class UsersSmokeTest(unittest.TestCase):

    SERVER = 'http://localhost:8069'
    DATABASE = 'nhclinical'
    USER = 'adt'
    PASSWORD = 'adt'

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

        self.senior_ids = self.client.read('res.groups',
                                       [('name','=',
                                         'NH Clinical Senior Manager Group')],
                                       'users')
        self.senior_managers = len(self.senior_ids[0])

        self.kiosk_ids = self.client.read('res.groups',
                                          [('name', '=',
                                            'NH Clinical Kiosk Group')],
                                       'users')
        self.kiosks = len(self.kiosk_ids[0])

        self.wards = self.client.read('nh.clinical.location',
                                        [('usage', '=', 'ward')])

        patients = self.client.model('nh.clinical.patient')
        self.patients = patients.search([])

        self.ward_names = []
        for ward in self.wards:
              self.ward_names.append(ward['name'])

        self.patients_in_ward = 0
        for ward in self.wards:
            self.patients_in_ward += len(ward['patient_ids'])

        self.nurse_list = []
        for ward in self.wards:
            self.nurse_list.append(ward['assigned_nurse_ids'])

        self.doctor_list = []
        for ward in self.wards:
            self.doctor_list.append(ward['assigned_doctor_ids'])

        self.hca_list = []
        for ward in self.wards:
            self.hca_list.append(ward['related_hcas'])

        self.beds = self.client.read('nh.clinical.location',
                                     [('usage', '=', 'bed')])
        self.bed_total = []
        for ward in self.wards:
            self.bed_list = []
            for bed in self.beds:
               if ward['name'] in bed['full_name']:
                 self.bed_list.append(bed)
            self.bed_total.append(len(self.bed_list))

        self.list_patients_in_bed = []
        for ward in self.wards:
            self.patients_in_bed = 0
            for bed in self.beds:
                if ward['name'] in bed['full_name']:
                    if bed['is_available'] is False:
                        self.patients_in_bed += 1
            self.list_patients_in_bed.append(self.patients_in_bed)


    def test_hospital_name(self):
        """Asserts that the hospital name is correct"""
        self.assertEqual(self.hospital, 'Greenfield University Hospital',
                         'Incorrect hospital name')

    def test_senior_managers(self):
        """Asserts that there are the correct amount of senior managers"""
        self.assertEqual(self.senior_managers, 3,
                         'Incorrect amount of managers')

    def test_wards(self):
        """Asserts that there are 5 wards, named A-E respectively"""
        self.assertEqual(self.ward_names,
                         ['Ward A', 'Ward B', 'Ward C', 'Ward D', 'Ward E'],
                         'Incorrect ward names')

    def test_total_patients_in_ward(self):
        """Asserts that the wards have a total of 180 patients"""
        self.assertEqual(self.patients_in_ward, 180,
                         'Incorrect total of patients in ward')

    def test_total_patients(self):
        """Asserts that there are 200 patients registered"""
        self.assertEqual(len(self.patients), 200, 'Incorrect total patients')

    def test_ward_nurses(self):
        """Asserts that there are 10 nurses in each ward"""
        for ward in self.wards:
            for list in self.nurse_list:
                self.assertEqual(len(list), 10,
                                 'Incorrect number of nurses in ' +
                                 ward['name'])

    def test_ward_doctors(self):
        """Asserts that there are 4 doctors in each ward"""
        for ward in self.doctor_list:
            self.assertEqual(len(ward), 4, 'Incorrect number of doctors')

    def test_ward_hcas(self):
        """Asserts that there are 10 hcas in each ward"""
        for hca in self.hca_list:
            self.assertEqual(hca, 10, 'Incorrect number of hcas')

    def test_beds(self):
        """Asserts that there are 30 beds in each ward"""
        for beds in self.bed_total:
            self.assertEqual(beds, 30, 'Incorrect number of beds')

    def test_patients_in_bed(self):
        """Asserts that there are 28 patients in a bed, in each ward"""
        for ward in self.list_patients_in_bed:
            self.assertEqual(ward, 28, 'Incorrect number of patients in bed')

    def test_kiosks(self):
        """Asserts that there are the correct number of kiosks"""
        self.assertEqual(self.kiosks, 5, 'Incorrect number of kiosks')

    def test_discharged_patients(self):
        """Asserts there are 20 discharged patients"""
        location = self.client.model('nh.clinical.location')
        discharge_location_id = location.search([('code', '=', 'DISL-GUH')])
        patient = self.client.model('nh.clinical.patient')
        dicharged_patients_ids = patient.search(
            [('current_location_id', '=', discharge_location_id)]
        )

        self.assertEqual(len(dicharged_patients_ids), 20)

    def test_transferred_patients(self):
        """Asserts there have been 20 transfers"""
        transfer_pool = self.client.model('nh.clinical.patient.transfer')
        transfer_ids = transfer_pool.search([])
        self.assertEqual(len(transfer_ids), 20)


if __name__ == '__main__':
    unittest.main()
