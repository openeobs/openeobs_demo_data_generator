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
            client = erppeek.Client(server, db=db, user=user,
                                    password=password, verbose=False)
        except:
            raise RuntimeError(
                "Error connecting to {0} on {1} "
                "using credentials {2}:{3}".format(db, server, user, password)
            )
        return client


class DischargeTransferCoordinator(object):

    def __init__(self, server, database, user, password):
        client = get_erppeek_client(server=server, db=database, user=user,
                                    password=password)

        # go two-by-two as ward already has 28 patients placed (max 30)
        for i in range(2):
            DischargePatients(client, 'A', 2)
            DischargePatients(client, 'B', 2)
            DischargePatients(client, 'C', 2)
            DischargePatients(client, 'D', 2)
            DischargePatients(client, 'E', 2)

        TransferPatients(client, 'A', 'B', 4)
        TransferPatients(client, 'B', 'C', 4)
        TransferPatients(client, 'C', 'D', 4)
        TransferPatients(client, 'D', 'E', 4)
        TransferPatients(client, 'E', 'A', 4)


class DischargePatients(object):

    def __init__(self, client, discharge_ward, patients_to_affect):
        self.client = client
        self.discharge_patients(discharge_ward, patients_to_affect)

    def discharge_patients(self, ward, patients):
        api_demo = self.client.model('nh.eobs.demo.loader')
        api_demo.discharge_patients(ward, patients)


class TransferPatients(object):

    def __init__(self, client, from_ward, to_ward, patients):
        self.client = client
        self.transfer_patients(from_ward, to_ward, patients)

    def transfer_patients(self, from_ward, to_ward, patients):
        api_demo = self.client.model('nh.eobs.demo.loader')
        api_demo.transfer_patients(from_ward, to_ward, patients)
