import unittest
from mock import MagicMock, Mock
from analysis_tools.user import User

class TestUserBuilder(unittest.TestCase):
    """
    Test that the user class builds user structure correctly
    """

    def setUp(self):
        self.mock_client = MagicMock()
        mock_model = MagicMock()
        self.mock_client.model = MagicMock(return_value=mock_model)

        def read(id, fields):
            if fields[0] == 'name':
                if id == 1:
                    return {'id': id, 'name': 'Doctor'}
                else:
                    return {'id': id, 'name': 'Nurse'}
            else:
                if id == 1:
                    return {'id': id, 'category_id': [1]}
                else:
                    return {'id': id, 'category_id': [1, 2]}

        mock_model.read = read

    def test_build_user(self):
        user = User(self.mock_client, 1)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, 'Doctor')
        self.assertListEqual(user.roles, ['Doctor'])

    def test_csv_list(self):
        user = User(self.mock_client, 1)
        self.assertListEqual(
            user.csv_list(), [1, 'Doctor', 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
