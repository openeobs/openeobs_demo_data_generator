import argparse
import sys

from assign_users_to_spells import (ReallocateUsersToWards,
                                    ReallocateUsersToBeds)
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
    # Re-allocate users to their current locations,
    # to fix the problem about patients not showing up in the Acuity Board.
    beds_reallocator = ReallocateUsersToBeds(server, database, 'oakley',
                                             'oakley')
    beds_reallocator.reallocate_all_users()
    wards_reallocator = ReallocateUsersToWards(server, database, 'oakley',
                                               'oakley')
    wards_reallocator.reallocate_all_users()
    DischargeTransferCoordinator(server, database, 'adt', 'adt')


if __name__ == '__main__':
    sys.exit(main())
