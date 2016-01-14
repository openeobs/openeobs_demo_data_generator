import sys
import argparse

from assign_users_to_spells import ReallocateUsersToWards
from discharge_transfer import DischargeTransferCoordinator


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
    reallocator = ReallocateUsersToWards(server, database, 'oakley', 'oakley')
    reallocator.reallocate_all_users()
    DischargeTransferCoordinator(server, database, 'adt', 'adt')


if __name__ == '__main__':
    sys.exit(main())
