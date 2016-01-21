from erppeek import Client
from datetime import datetime
from demo_setup_tools.assign_users_to_spells import (ReallocateUsersToBeds,
                                                     ReallocateUsersToWards)
from demo_setup_tools.discharge_transfer import DischargeTransferCoordinator
from read_demo_data import UsersSmokeTest, MobileSmokeTest
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
        client = Client(server, db=db, user=user, password=password,
                                verbose=False)
    except:
        raise RuntimeError(
            "Error connecting to {0} on {1} using credentials {2}:{3}".format(
                db, server, user, password
            )
        )
    return client


class RefreshDemo(object):
    """
    A class that handles refreshing an existing instance of Open eObs
    """

    def __init__(self, server, database, user, password, admin_password,
                 db_admin):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.admin_password = admin_password
        self.db_admin = db_admin
        self.temp_db_name = datetime.strftime('nhclinical_%Y%m%d')
        self.client = get_erppeek_client(server, db=database, user=user,
                                         password=password)
        # Check to make sure specified database exists
        if not self.check_database(database):
            raise RuntimeError('Database not found on server')
        # Create a new database to install Open eObs onto
        if not self.create_new_db():
            raise RuntimeError('Error creating new database')
        # Install Open eObs
        self.client = get_erppeek_client(server, db=self.temp_db_name,
                                         user=user, password='admin')
        if not self.install_eobs():
            raise RuntimeError('Error installing Open eObs')
        # Run post setup scripts against open eObs
        self.post_install_setup()
        # Run smoke tests against open eObs
        self.run_smoke_tests()
        # If we all good then rename specified database
        old_db_name = '{0}_old'.format(self.database)
        if not self.rename_database(self.database,
                                    old_db_name):
            raise RuntimeError('Error renaming old database')
        # Rename new database
        if not self.rename_database(self.temp_db_name, self.database):
            self.rename_database(old_db_name, self.database)
            raise RuntimeError('Error renaming new database, reverting old')
        # Drop the old database - will return true if database still there
        if self.remove_old_database(self.database):
            raise RuntimeError('Error removing old database')

    def check_database(self, database):
        """
        Return if the specified database is in available
        :param database: Name of DB to check for
        :return: Boolean if is there or not
        """
        return self.client.db.db_exist(database)

    def create_new_db(self):
        """
        Create a new database
        :return: True if successful
        """
        self.client.db.create_database(self.db_admin, self.temp_db_name)
        return self.check_database(self.temp_db_name)

    def install_eobs(self):
        """
        Install the Open eObs application
        :return: True if successful
        """
        self.client.install('nh_eobs_mobile')
        mob_installed = self.client.modules('nh_eobs_mobile')
        if 'nh_eobs_mobile' not in mob_installed['installed']:
            return False
        self.client.install('nh_eobs_demo')
        demo_installed = self.client.modules('nh_eobs_demo')
        if 'nh_eobs_demo' not in demo_installed['installed']:
            return False
        return True

    def post_install_setup(self):
        """
        Reallocate users to beds and wards and discharge / transfer some
        patients
        """
        beds_reallocator = ReallocateUsersToBeds(self.server,
                                                 self.temp_db_name,
                                                 'oakley', 'oakley')
        beds_reallocator.reallocate_all_users()
        wards_reallocator = ReallocateUsersToWards(self.server,
                                                   self.temp_db_name,
                                                   'oakley',  'oakley')
        wards_reallocator.reallocate_all_users()
        DischargeTransferCoordinator(self.server, self.temp_db_name, 'adt',
                                     'adt')

    def run_smoke_tests(self):
        """
        Run some post deployment smoke tests
        """
        UsersSmokeTest.SERVER = self.server
        UsersSmokeTest.DATABASE = self.temp_db_name
        UsersSmokeTest.USER = 'adt'
        UsersSmokeTest.PASSWORD = 'adt'

        suite = unittest.TestLoader().loadTestsFromTestCase(UsersSmokeTest)
        unittest.TextTestRunner(verbosity=2).run(suite)

        MobileSmokeTest.SERVER = self.server
        MobileSmokeTest.DATABASE = self.temp_db_name
        MobileSmokeTest.USER = 'nasir'
        MobileSmokeTest.PASSWORD = 'nasir'

        suite = unittest.TestLoader().loadTestsFromTestCase(MobileSmokeTest)
        unittest.TextTestRunner(verbosity=2).run(suite)

    def rename_database(self, current_name, new_name):
        """
        Rename a database
        :param current_name: The current name of the database
        :param new_name: The name to call the database after operation
        :return: Boolean of if successful or not
        """
        self.client.db.rename(self.db_admin, current_name, new_name)
        return self.check_database(new_name)

    def remove_old_database(self, db_to_drop):
        """
        Remove (drop) the old DB
        :param db_to_drop: The database to drop
        :return: if drop worked
        """
        self.client.db.drop(self.db_admin, db_to_drop)
        return self.check_database(db_to_drop)
