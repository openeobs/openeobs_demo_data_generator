import argparse
import sys
from demo_refresh_tools.refresh_demo import RefreshDemo


PARSER = argparse.ArgumentParser('Refresh an existing Open eObs demo instance')
PARSER.add_argument('--database', type=str,
                    help='Database to run against',
                    default='nhclinical')
PARSER.add_argument('--server', type=str,
                    help='Server to run against',
                    default='http://localhost:8069')
PARSER.add_argument('--user', type=str,
                    help='User to run as',
                    default='admin')
PARSER.add_argument('--password', type=str,
                    help='Password for user', default='admin')
PARSER.add_argument('--adminpassword', type=str,
                    help='New password for admin', default='admin')
PARSER.add_argument('--dbadmin', type=str,
                    help='Database Admin Password', default='admin')


def main():
    args = PARSER.parse_args()
    server = args.server
    database = args.database
    user = args.user
    password = args.password
    admin_password = args.adminpassword
    db_admin = args.dbadmin
    RefreshDemo(server, database=database, user=user, password=password,
                admin_password=admin_password, db_admin=db_admin)


if __name__ == '__main__':
    sys.exit(main())
