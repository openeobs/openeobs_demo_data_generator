import sys
import unittest
import argparse
from smoke_test_production import SmokeTestProduction

PARSER = argparse.ArgumentParser('Production smoke tests')
PARSER.add_argument('database', type=str, help='Database to run tests against', default='nhclinical')
PARSER.add_argument('--server', type=str, help='Server to run tests against', default='http://localhost:8069')
PARSER.add_argument('--admin-user', type=str, help='Admin username', default='admin')
PARSER.add_argument('--admin-pw', type=str, help='Admin user password')
PARSER.add_argument('--adt-user', type=str, help='ADT username', default='adt')
PARSER.add_argument('--adt-pw', type=str, help='ADT user password')

def main():
    args = PARSER.parse_args()
    SmokeTestProduction.SERVER = args.server
    SmokeTestProduction.DATABASE = args.database
    SmokeTestProduction.ADMIN_USER = 'admin'
    SmokeTestProduction.ADMIN_PASSWORD = 'admin'
    SmokeTestProduction.ADT_USER = 'adt'
    SmokeTestProduction.ADT_PASSWORD = 'adt'

    suite = unittest.TestLoader().loadTestsFromTestCase(SmokeTestProduction)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    sys.exit(main())
