import sys
import unittest
import argparse
from smoke_test_production import SmokeTestProduction

PARSER = argparse.ArgumentParser('Production smoke tests')
PARSER.add_argument('database', type=str,
                    help='Database to run tests against',
                    default='nhclinical')
PARSER.add_argument('--server', type=str,
                    help='Server to run tests against',
                    default='http://54.171.180.53')
PARSER.add_argument('--user', type=str,
                    help='User to run tests as',
                    default='admin')
PARSER.add_argument('--password', type=str,
                    help='Password for testing user', default='admin')


def main():
    args = PARSER.parse_args()
    SmokeTestProduction.SERVER = args.server
    SmokeTestProduction.DATABASE = args.database
    SmokeTestProduction.USER = 'admin'
    SmokeTestProduction.PASSWORD = 'admin'

    suite = unittest.TestLoader().loadTestsFromTestCase(SmokeTestProduction)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    sys.exit(main())
