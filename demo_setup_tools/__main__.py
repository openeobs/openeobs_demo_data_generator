import sys
import argparse
from assign_users_to_spells import ReallocateWardManagers
from observations import SubmitObservations

PARSER = argparse.ArgumentParser('Post Open-eObs Demo installation operations')
PARSER.add_argument('database', type=str,
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
PARSER.add_argument('--days', type=int, help='Number of days for observation',
                    default=2)


def main():
    args = PARSER.parse_args()
    server = args.server
    database = args.database
    user = args.user
    password = args.password
    days = args.days
    ReallocateWardManagers(server, database, 'olga', 'olga')
    SubmitObservations(server, database, user, password, days)


if __name__ == '__main__':
    sys.exit(main())
