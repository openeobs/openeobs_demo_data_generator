import argparse
import sys
from analysis_tools.user_analysis import UserAnalysis


PARSER = argparse.ArgumentParser(
    'Analyze user data from an Open eObs database')
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
PARSER.add_argument('--filename', type=str,
                    help='Path to CSV file to save analysis to',
                    default='user_list.csv')


def main():
    args = PARSER.parse_args()
    server = args.server
    database = args.database
    user = args.user
    password = args.password
    filename = args.filename
    ua = UserAnalysis(server, database=database, user=user, password=password)
    ua.export_csv_users(filename)


if __name__ == '__main__':
    sys.exit(main())
