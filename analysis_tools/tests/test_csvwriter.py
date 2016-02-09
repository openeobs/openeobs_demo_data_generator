import os
import csv
from unittest import TestCase

from analysis_tools.csvwriter import column_names, add_column_names, \
    create_user_csv


class TestUserCSVWriter(TestCase):

    def setUp(self):
        self.users = [
            [1, 'nora', 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [2, 'waino', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.field_names = [
            'user_id', 'username', 'System Administrator', 'Kiosk',
            'Senior Manager', 'Receptionist', 'Doctor', 'Senior Doctor',
            'Junior Doctor', 'Registrar', 'Consultant', 'Ward Manager',
            'Nurse', 'HCA'
        ]

    def tearDown(self):
        try:
            os.remove('test.csv')
        except OSError:
            pass

    def test_column_names_returns_list_of_column_names(self):
        self.assertEqual(column_names(), self.field_names)

    def test_add_column_names_prepends_column_names_to_list_of_users(self):
        users = list(self.users)

        add_column_names(users)

        self.assertNotEqual(users, self.users)
        self.assertEqual(users[0], self.field_names)
        self.assertEqual(users[1], self.users[0])
        self.assertEqual(users[2], self.users[1])

    def test_create_user_csv_creates_a_csv_file(self):
        create_user_csv('test.csv', self.users)
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