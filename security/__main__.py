import sys
import argparse
from change_admin_password import ChangeAdminPassword

PARSER = argparse.ArgumentParser('Secure Odoo once setup')
PARSER.add_argument('database', type=str,
                    help='Database to run against',
                    default='nhclinical')
PARSER.add_argument('--password', type=str,
                    help='Password for user')
PARSER.add_argument('--dbpassword', type=str,
                    help='Password for user')


def main():
    args = PARSER.parse_args()
    database = args.database
    new_password = args.password
    admin_password = args.dbpassword
    ChangeAdminPassword(database, new_password, admin_password)


if __name__ == '__main__':
    sys.exit(main())
