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


class SmokeTest(unittest.TestCase):

    SERVER = 'http://localhost:8069'
    DATABASE = 'nhclinical'
    USER = 'adt'
    PASSWORD = 'adt'

    def setUp(self):
        self.client = get_erppeek_client(
            server=self.SERVER, db=self.DATABASE,
            user=self.USER, password=self.PASSWORD
        )
        self.user_pool = self.client.model('res.users')
        self.location_pool = self.client.model('nh.clinical.location')
        self.patient_pool = self.client.model('nh.clinical.patient')
        self.activity_pool = self.client.model('nh.activity')
        self.hospital_pos = self.client.search(
            'nh.clinical.location', [['code', '=', 'GUH']])
        self.hospital_search = self.client.search(
            'nh.clinical.pos', [['location_id', 'in', self.hospital_pos]])[0]
        self.senior_ids = self.client.read(
            'res.groups', [('name', '=', 'NH Clinical Senior Manager Group')],
            'users')
        self.senior_managers = len(self.senior_ids[0])
        self.wards = self.client.read(
            'nh.clinical.location', [('usage', '=', 'ward')])
        self.beds = self.client.read(
            'nh.clinical.location', [('usage', '=', 'bed')])

    def test_user_is_responsible_for_locations_expected(self):
        """Asserts user is responsible for locations"""
        user_ids = self.user_pool.search([('login', '=', 'nasir')])
        user = self.user_pool.browse(user_ids[0])

        location_ids = user.location_ids
        self.assertTrue(len(location_ids), 3)

        self.assertEqual(location_ids[0].name, 'Bed 1')
        self.assertEqual(location_ids[1].name, 'Bed 2')
        self.assertEqual(location_ids[2].name, 'Bed 3')

    def test_patients_placed_in_beds_expected(self):
        """Asserts patients are placed in beds expected"""
        bed_id = self.location_pool.search([('code', '=', 'A1')])
        bed = self.location_pool.browse(bed_id)

        patient_ids = bed.patient_ids
        self.assertEquals(len(patient_ids), 1)

    def test_patients_have_scheduled_observation_expected(self):
        """Asserts patients have a scheduled observations"""
        patient_ids = self.patient_pool.search(
            [('other_identifier', '=', 'HOSNUM0002')])
        ews_ids = self.activity_pool.search(
            [
                ('data_model', '=', 'nh.clinical.patient.observation.ews'),
                ('patient_id', 'in', patient_ids), ('state', '=', 'scheduled')
            ])

        self.assertEqual(len(ews_ids), 1)

    def test_patients_have_medical_team_notifications(self):
        """Asserts patients have medical team notificaitons"""
        patient_ids = self.patient_pool.search([])
        medical_notification_ids = self.activity_pool.search(
            [
                ('data_model', '=', 'nh.clinical.notification.medical_team'),
                ('patient_id', 'in', patient_ids)
            ])
        self.assertTrue(len(medical_notification_ids) > 0)

    def test_patients_have_assessment_notifications(self):
        """Asserts patients have assessment notifications"""
        patient_ids = self.patient_pool.search([])
        assessment_notification_ids = self.activity_pool.search(
            [
                ('data_model', '=', 'nh.clinical.notification.assessment'),
                ('patient_id', 'in', patient_ids)
            ])
        self.assertTrue(len(assessment_notification_ids) > 0)

    def test_hospital_name(self):
        """Asserts that the hospital name is correct"""
        self.hospital = self.client.read(
            'nh.clinical.pos', self.hospital_search, ['name'])['name']
        self.assertEqual(self.hospital, 'Greenfield University Hospital',
                         'Incorrect hospital name')

    def test_senior_managers_is_3(self):
        """Asserts that there are 3 senior managers"""
        self.assertEqual(self.senior_managers, 3,
                         'Incorrect amount of managers')

    def test_wards_are_named_A_to_E(self):
        """Asserts that there are 5 wards, named A-E respectively"""
        ward_names = [ward['name'] for ward in self.wards]
        self.assertEqual(
            ward_names,
            ['Ward A', 'Ward B', 'Ward C', 'Ward D', 'Ward E'],
            'Incorrect ward names')

    def test_total_patients_placed_is_180(self):
        """Asserts that the wards have a total of 180 patients"""
        patients_in_ward = 0
        for ward in self.wards:
            patients_in_ward += len(ward['patient_ids'])
        self.assertEqual(patients_in_ward, 180,
                         'Incorrect total of patients in ward')

    def test_total_patients_is_200(self):
        """Asserts that there are 200 patients registered"""
        patients = self.client.model('nh.clinical.patient')
        self.patients = patients.search([])
        self.assertEqual(len(self.patients), 200, 'Incorrect total patients')

    def test_ward_nurses_is_10_per_ward(self):
        """Asserts that there are 10 nurses in each ward"""
        nurse_lists = [ward['assigned_nurse_ids'] for ward in self.wards]
        for ward in self.wards:
            for nurse_list in nurse_lists:
                self.assertEqual(
                    len(nurse_list), 10,
                    'Incorrect number of nurses in ' + ward['name'])

    def test_ward_doctors_is_4_per_ward(self):
        """Asserts that there are 4 doctors in each ward"""
        doctor_list = [ward['assigned_doctor_ids'] for ward in self.wards]
        for ward in doctor_list:
            self.assertEqual(len(ward), 4, 'Incorrect number of doctors')

    def test_ward_hcas_is_10_per_ward(self):
        """Asserts that there are 10 hcas in each ward"""
        hca_list = [ward['related_hcas'] for ward in self.wards]
        for hca in hca_list:
            self.assertEqual(hca, 10, 'Incorrect number of hcas')

    def test_beds_in_ward_is_30_per_ward(self):
        """Asserts that there are 30 beds in each ward"""
        bed_total = []
        for ward in self.wards:
            bed_list = []
            for bed in self.beds:
                if ward['name'] in bed['full_name']:
                    bed_list.append(bed)
            bed_total.append(len(bed_list))

        for beds in bed_total:
            self.assertEqual(beds, 30, 'Incorrect number of beds')

    def test_patients_in_bed_is_28_per_ward(self):
        """Asserts that there are 28 patients in a bed, in each ward"""
        list_patients_in_bed = []
        for ward in self.wards:
            patients_in_bed = 0
            for bed in self.beds:
                if ward['name'] in bed['full_name']:
                    if bed['is_available'] is False:
                        patients_in_bed += 1
            list_patients_in_bed.append(patients_in_bed)

        for ward in list_patients_in_bed:
            self.assertEqual(ward, 28, 'Incorrect number of patients in bed')

    def test_kiosk_users_is_5(self):
        """Asserts that there are 5 kiosk users"""
        kiosk_ids = self.client.read(
            'res.groups', [('name', '=', 'NH Clinical Kiosk Group')], 'users')
        self.assertEqual(len(kiosk_ids[0]), 5, 'Incorrect number of kiosks')

    def test_discharged_patients_is_20(self):
        """Asserts there are 20 discharged patients"""
        location = self.client.model('nh.clinical.location')
        discharge_location_id = location.search([('code', '=', 'DISL-GUH')])
        patient = self.client.model('nh.clinical.patient')
        dicharged_patients_ids = patient.search(
            [('current_location_id', '=', discharge_location_id)]
        )
        self.assertEqual(len(dicharged_patients_ids), 20)

    def test_transferred_patients_is_20(self):
        """Asserts there have been 20 transfers"""
        transfer_pool = self.client.model('nh.clinical.patient.transfer')
        transfer_ids = transfer_pool.search([])
        self.assertEqual(len(transfer_ids), 20)


if __name__ == '__main__':
    unittest.main()
