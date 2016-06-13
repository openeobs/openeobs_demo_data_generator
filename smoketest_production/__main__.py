import sys
import unittest
import argparse
import erppeek
from smoke_test_production import ParametrizedTest
from smoke_test_production import ADT

PARSER = argparse.ArgumentParser('Production smoke tests')
PARSER.add_argument('database', type=str, help='Database to run tests against', default='nhclinical')
PARSER.add_argument('--server', type=str, help='Server to run tests against', default='http://localhost:8069')
PARSER.add_argument('--adminuser', type=str, help='Admin username', default='admin')
PARSER.add_argument('--adminpw', type=str, help='Admin user password')
PARSER.add_argument('--adtuser', type=str, help='ADT username', default='adt')
PARSER.add_argument('--adtpw', type=str, help='ADT user password')


def main():
    args = PARSER.parse_args()
    server = args.server
    db = args.database
    admin_user = args.adminuser
    admin_password = args.adminpw
    adt_user = args.adtuser
    adt_password = args.adtpw
    test_database = 'nhclinical_duplicate'

    print server
    print db
    print admin_user
    print admin_password

    #client = erppeek.Client(server=server, db=db, user=admin_user, password=admin_password)

    #if client.db.db_exist(test_database):
    #    client.db.drop(admin_user, test_database)
    #
    #client.db.duplicate_database(admin_user, db, test_database)

    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTest.parametrize(ADT, server=server))

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    sys.exit(main())
