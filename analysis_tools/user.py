class User(object):

    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.name = self.get_name()
        self.roles = self.get_roles()

    def get_name(self):
        return self.client.model('res.users').read(self.id, ['name'])['name']

    def get_roles(self):
        role_model = self.client.model('hr.employee.category')
        return []
