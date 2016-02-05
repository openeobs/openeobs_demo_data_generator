from unittest import TestCase

from demo_data_generators.user_names import UserNames, nurse_first_names


class TestUserNames(TestCase):

    def setUp(self):
        self.names = UserNames()

    def test_getitem_returns_generator_of_names(self):
        nurse_generator = self.names['nurse']
        self.assertEqual(nurse_generator, nurse_first_names)
