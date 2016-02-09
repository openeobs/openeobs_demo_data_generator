from erppeek import Client
from csvwriter import create_user_csv


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
    client = Client(server, db=db, user=user, password=password,
                    verbose=False)
    return client


class User(object):
    """
    A class that represents an Odoo user object and maps id with name and
    Open eObs user roles
    """

    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.name = self.fetch_name()
        self.roles = self.fetch_roles()

    def fetch_name(self):
        return self.client.model('res.users').read(self.id, ['name'])['name']

    def fetch_roles(self):
        user_roles = self.client.model('res.users').read(
            self.id, ['category_id'])['category_id']
        role_model = self.client.model('res.partner.category')
        return [role_model.read(r, ['name'])['name'] for r in user_roles]

    def csv_list(self):
        roles = ['System Administrator', 'Kiosk', 'Senior Manager',
                 'Receptionist', 'Doctor', 'Senior Doctor', 'Junior Doctor',
                 'Registrar', 'Consultant', 'Ward Manager', 'Nurse', 'HCA']
        user_list = [self.id, self.name]
        for r in roles:
            if r in self.roles:
                user_list.append(1)
            else:
                user_list.append(0)
        return user_list


class UserAnalysis(object):
    """
    A class that handles analyzing user data from an Odoo database
    """

    def __init__(self, server, database, user, password):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.client = get_erppeek_client(server, db=database, user=user,
                                         password=password)
        user_ids = self.client.model('res.users').search([])
        self.users = [User(self.client, uid).csv_list() for uid in user_ids]

    def export_csv_users(self, filename):
        create_user_csv(filename, self.users)
