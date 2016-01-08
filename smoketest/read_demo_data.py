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

    def setUp(self):
        self.client = get_erppeek_client(server='http://localhost:8069',
                                    db='demo_data_master', user='admin',
                                    password='admin')

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

        self.list_patients_in_bed = []
        for ward in self.wards:
            self.patients_in_bed = 0
            for bed in self.beds:
                if ward['name'] in bed['full_name']:
                    if bed['is_available'] is False:
                        self.patients_in_bed += 1
            self.list_patients_in_bed.append(self.patients_in_bed)

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
        for ward in self.doctor_list:
            self.assertEqual(len(ward), 4, 'Incorrect number of doctors')

    def test_ward_hcas(self):
        for hca in self.hca_list:
            self.assertEqual(hca, 10, 'Incorrect number of hcas')

    def test_beds(self):
        for beds in self.bed_total:
            self.assertEqual(beds, 30, 'Incorrect number of beds')

    def test_patients_in_bed(self):
        for ward in self.list_patients_in_bed:
            self.assertEqual(ward, 28, 'Incorrect number of patients in bed')




    # def test_read_data(client):
    # """Read a list of ward names"""
    #
    # #Print hospital name
    # print('Hospital: {hospital}').format(hospital=)
    #
    # #Print the amount of senior managers
    # sen_managers = client.read('res.partner.category', [('name','=','Senior Manager')], 'child_ids')
    # print('Senior Managers: {senior}').format(senior=len(sen_managers[0]))
    #
    # #Read the record of each ward, and print information
    # records = client.read('nh.clinical.location', [('usage', '=', 'ward')])
    # for record in records:
    #
    #     #Print name of ward and number of patients in each ward
    #     print(record['name'])
    #     print('Patients: {patients}'.format(patients=len(record['patient_ids'])))
    #
    #     #Print number of beds in each ward
    #     beds = client.read('nh.clinical.location', [('usage', '=', 'bed')])
    #     bed_list = []
    #     for bed in beds:
    #         if record['name'] in bed['full_name']:
    #             bed_list.append(bed)
    #     print('Beds: {beds}'.format(beds=len(bed_list)))
    #
    #     #Print number of nurses in each ward
    #     nurse_list = []
    #     for nurse_id in record['assigned_nurse_ids']:
    #         nurse_name = client.read('res.users', [('id', '=', nurse_id)],'display_name')
    #         nurse_list.append(nurse_name)
    #     print('Nurses: {nurses}'.format(nurses=len(nurse_list)))
    #
    #     #Print number of doctors in each ward
    #     doctor_list = []
    #     for doctor_id in record['assigned_doctor_ids']:
    #         doctor_name = client.read('res.users', [('id', '=', doctor_id)],'display_name')
    #         doctor_list.append(doctor_name)
    #     print('Doctors: {doctors}'.format(doctors=len(doctor_list)))
    #
    #     print("HCAs: {hca}").format(hca=record['related_hcas'])
    #
    #     print('')

if __name__ == '__main__':
    unittest.main()