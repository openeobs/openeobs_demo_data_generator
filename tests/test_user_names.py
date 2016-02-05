import types
from unittest import TestCase


from demo_data_generators.user_names import UserNames


class TestUserNames(TestCase):

    def setUp(self):
        self.names = UserNames()

    def test_getitem_returns_generator_of_names(self):
        nurse_generator = self.names['nurse']
        self.assertEqual(type(nurse_generator), types.GeneratorType)

    def test_setitem_assigns_key_value_pair(self):
        self.names['nurse'] = (i for i in ['Nadine'])
        self.assertEqual(self.names['nurse'].next(), 'Nadine')
