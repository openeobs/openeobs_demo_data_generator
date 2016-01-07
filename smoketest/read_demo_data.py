import erppeek


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



def read_data(client):
    """Read a list of ward names"""

    #Print hospital name
    print('Hospital: {hospital}').format(hospital=client.read('nh.clinical.pos', [('name', '=', 'Greenfield University Hospital')], 'name'))

    #Print the amount of senior managers
    sen_managers = client.read('res.partner.category', [('name','=','Senior Manager')], 'child_ids')
    print('Senior Managers: {senior}').format(senior=len(sen_managers[0]))

    #Read the record of each ward, and print information
    records = client.read('nh.clinical.location', [('usage', '=', 'ward')])
    for record in records:

        #Print name of ward and number of patients in each ward
        print(record['name'])
        print('Patients: {patients}'.format(patients=len(record['patient_ids'])))

        #Print number of beds in each ward
        beds = client.read('nh.clinical.location', [('usage', '=', 'bed')])
        bed_list = []
        for bed in beds:
            if record['name'] in bed['full_name']:
                bed_list.append(bed)
        print('Beds: {beds}'.format(beds=len(bed_list)))

        #Print number of nurses in each ward
        nurse_list = []
        for nurse_id in record['assigned_nurse_ids']:
            nurse_name = client.read('res.users', [('id', '=', nurse_id)],'display_name')
            nurse_list.append(nurse_name)
        print('Nurses: {nurses}'.format(nurses=len(nurse_list)))

        #Print number of doctors in each ward
        doctor_list = []
        for doctor_id in record['assigned_doctor_ids']:
            doctor_name = client.read('res.users', [('id', '=', doctor_id)],'display_name')
            doctor_list.append(doctor_name)
        print('Doctors: {doctors}'.format(doctors=len(doctor_list)))

        print("HCAs: {hca}").format(hca=record['related_hcas'])

        print('')


client = database_connect('http://localhost:8069', 'demo_data_master', 'norah')
read_data(client)
