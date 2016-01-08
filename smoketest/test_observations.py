# coding=utf-8
import erppeek
import unittest
from demo_setup_tools.observations import SubmitInitialObservations, \
    SubmitFinalObservations



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

class ObservationsSmokeTest(unittest.TestCase):

    SERVER = 'http://localhost:8069'
    DATABASE = 'nhclinical'
    USER = 'admin'
    PASSWORD = 'admin'

    def setUp(self):
        self.client = get_erppeek_client(server=self.SERVER, db=self.DATABASE,
                                         user=self.USER, password=self.PASSWORD)

    def test_SubmitInitialObservations(self):
        SubmitInitialObservations(self.client, 1)

    def test_SubmitFinalObservations(self):
        SubmitFinalObservations(self.client, 1)
