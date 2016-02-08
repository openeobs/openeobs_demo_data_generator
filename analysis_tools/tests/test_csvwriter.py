import os
import csv
from unittest import TestCase

from analysis_tools.csvwriter import UserCSVWriter


class TestUserCSVWriter(TestCase):

    def setUp(self):
        self.users = [
            [1, 'nora', 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [2, 'waino', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def tearDown(self):
        os.remove('test.csv')

    def test_UserCSVWriter_writes_to_file(self):
        UserCSVWriter('test.csv', self.users)
        with open('test.csv', 'rb') as f:
            reader = csv.DictReader(f)
            row = reader.next()
            self.assertEqual(row['user_id'], '1')
            self.assertEqual(row['username'], 'nora')
            self.assertEqual(row['System Administrator'], '1')
            row = reader.next()
            self.assertEqual(row['user_id'], '2')
            self.assertEqual(row['username'], 'waino')
            self.assertEqual(row['Kiosk'], '0')
