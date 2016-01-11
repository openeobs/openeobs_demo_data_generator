import unittest
from demo_data_generators.users import UsersGenerator


class TestUserGeneratorNames(unittest.TestCase):
    """
    Test that the names provided by the UsersGenerator class are working
    """

    def setUp(self):
        gen = UsersGenerator({})
        names_list = gen.names_generators
        self.hca_names = names_list['hca']
        self.nurse_names = names_list['nurse']
        self.ward_manager_names = names_list['ward_manager']
        self.senior_manager_names = names_list['senior_manager']
        self.doctor_names = names_list['doctor']
        self.kiosk_names = names_list['kiosk']
        self.admin_names = names_list['admin']

    def test_hca_names(self):
        """
        Make sure that the HCA names all begin with H
        """
        h_set = set()
        for item in self.hca_names:
            h_set.add(item[:1])
        self.assertEqual(h_set, set('H'),
                         'Incorrect names for HCA in generator')

    def test_nurse_names(self):
        """
        Make sure that the Nurse names all begin with N
        """
        n_set = set()
        for item in self.nurse_names:
            n_set.add(item[:1])
        self.assertEqual(n_set, set('N'),
                         'Incorrect names for Nurse in generator')

    def test_ward_manager_names(self):
        """
        Make sure that the Ward Manager names all begin with Ward Manager
        """
        wm_set = set()
        for item in self.ward_manager_names:
            wm_set.add(item[:1])
        self.assertEqual(wm_set, set('W'),
                         'Incorrect names for Ward Manager in generator')

    def test_senior_manager_names(self):
        """
        Make sure that the Senior Manager names all begin with H
        """
        sm_set = set()
        for item in self.senior_manager_names:
            sm_set.add(item[:1])
        self.assertEqual(sm_set, set('S'),
                         'Incorrect names for Senior Manager in generator')

    def test_doctor_names(self):
        """
        Make sure that the Doctor names all begin with D
        """
        d_set = set()
        for item in self.doctor_names:
            d_set.add(item[:1])
        self.assertEqual(d_set, set('D'),
                         'Incorrect names for Doctor in generator')

    def test_kiosk_names(self):
        """
        Make sure that the Kiosk names all begin with K
        """
        k_set = set()
        for item in self.kiosk_names:
            k_set.add(item[:1])
        self.assertEqual(k_set, set('K'),
                         'Incorrect names for Kiosk in generator')

    def test_admin_names(self):
        """
        Make sure that the Admin names all begin with O
        """
        o_set = set()
        for item in self.admin_names:
            o_set.add(item[:1])
        self.assertEqual(o_set, set('O'),
                         'Incorrect names for Open-eObs Admin in generator')
