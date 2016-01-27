import argparse
import sys

from discharge_transfer import DischargeTransferCoordinator
from db_operations import refresh_materialized_views

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
    DischargeTransferCoordinator(server, database, 'adt', 'adt')
    refresh_materialized_views()


if __name__ == '__main__':
    sys.exit(main())
