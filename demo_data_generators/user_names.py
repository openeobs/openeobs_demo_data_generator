hca_first_names = (
    'Hope', 'Helios', 'Heidi', 'Harris', 'Hilary', 'Hamish',
    'Hettie', 'Hermes', 'Hunter', 'Hira', 'Howard', 'Harold',
    'Harvey', 'Hussein', 'Henley', 'Haley', 'Harriet', 'Hilda',
    'Horatius', 'Hermione', 'Hector', 'Holly', 'Honey', 'Huw',
    'Hiba', 'Honor', 'Hisham', 'Heather', 'Hilda', 'Helene',
    'Helen', 'Hannah', 'Humphrey', 'Hazel', 'Heather', 'Harriett',
    'Habib', 'Hugh', 'Hudson', 'Hubert', 'Hattie', 'Harry',
    'Haydn', 'Hank', 'Heston', 'Harlow', 'Henry', 'Heracles',
    'Hylas', 'Hercules', 'Henri', 'Hamza', 'Hugo', 'Hudson',
    'Harper'
)
nurse_first_names = (
    'Nicolas', 'Nicolette', 'Nyle', 'Nianh', 'Nemo', 'Neil',
    'Nicola', 'Noah', 'Nina', 'Norah', 'Nisa', 'Nadine',
    'Nate', 'Neve', 'Nisha', 'Nevaeh', 'Natalia', 'Nur',
    'Nessus', 'Nathan', 'Norbert', 'Nyasha', 'Nigel', 'Nikita',
    'Niall', 'Ning', 'Nasir', 'Noemi', 'Nancy', 'Nelson',
    'Neo', 'Nadim', 'Nick', 'Nisha', 'Nyla', 'Nolan',
    'Naomi', 'Nojus', 'Nicole', 'Nate', 'Niobe', 'Nichole',
    'Ned', 'Nadia', 'Neptune', 'Norton', 'Natasha', 'Nelly',
    'Naseem', 'Nicky', 'Neil', 'Noah', 'Nathan', 'Niamh',
    'Neville'
)
ward_manager_first_names = (
    'Winifred', 'Walter', 'Whitney', 'William', 'Wes', 'Willow'
)
doctor_first_names = (
    'Delores', 'Damien', 'Dale', 'Delilah', 'Don', 'Diego',
    'Dawson', 'Dalek', 'Daniella', 'Dafyd', 'Davina', 'Dave',
    'Don', 'Delia', 'Denzel', 'Darius', 'Diana', 'Dana',
    'Dara', 'Dawn', 'Dominique', 'Dakota', 'Daphne', 'Debby'
)
senior_manager_first_names = ('Scotty', 'Spencer', 'Sophia')
kiosk_first_names = ('Kevin', 'Kelly', 'Klara', 'Kane', 'Klaus')
admin_first_names = ('Olga', 'Ollie')


class UserNames(object):

    def __init__(self):
        self.hca = (name for name in hca_first_names)
        self.nurse = (name for name in nurse_first_names)
        self.ward_manager = (name for name in ward_manager_first_names)
        self.senior_manager = (name for name in senior_manager_first_names)
        self.doctor = (name for name in doctor_first_names)
        self.kiosk = (name for name in kiosk_first_names)
        self.admin = (name for name in admin_first_names)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
