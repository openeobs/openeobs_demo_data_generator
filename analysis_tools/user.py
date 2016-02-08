class User(object):

    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.name = self.fetch_name()
        self.roles = self.fetch_roles()

    def fetch_name(self):
        return self.client.model('res.users').read(self.id, ['name'])['name']

    def fetch_roles(self):
        user_roles = self.client.model('res.users').read(
            self.id, ['category_id'])['category_id']
        role_model = self.client.model('res.partner.category')
        return [role_model.read(r, ['name'])['name'] for r in user_roles]

    def csv_list(self):
        roles = ['System Administrator', 'Kiosk', 'Senior Manager',
                 'Receptionist', 'Doctor', 'Senior Doctor', 'Junior Doctor',
                 'Registrar', 'Consultant', 'Ward Manager', 'Nurse', 'HCA']
        user_list = [self.id, self.name]
        for r in roles:
            if r in self.roles:
                user_list.append(1)
            else:
                user_list.append(0)
        return user_list
