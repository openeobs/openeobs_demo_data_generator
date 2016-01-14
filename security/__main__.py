import sys
import argparse
from change_admin_password import ChangeAdminPassword

PARSER = argparse.ArgumentParser('Secure Odoo once setup')
PARSER.add_argument('database', type=str,
                    help='Database to run against',
                    default='nhclinical')
PARSER.add_argument('--password', type=str,
                    help='Password for user')
PARSER.add_argument('--server', type=str,
                    help='Server to change password for',
                    default='http://localhost:8069')


def main():
    args = PARSER.parse_args()
    server = args.server
    database = args.database
    new_password = args.password
    ChangeAdminPassword(server, db=database, pwd=new_password)


if __name__ == '__main__':
    sys.exit(main())
