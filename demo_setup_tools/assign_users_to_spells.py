import erppeek


def get_erppeek_client(server='http://localhost:8069', db='openerp',
                       user='admin', password='admin'):
    """
    Get a ERPPeek client for us to use, if one not available then close the
    function
    :param server: Server address (with XML-RPC port)
    :param db: Name of database
    :param user: Username to connect with
    :param password: Password for username connecting with
    :return: A erppeek.Client object we can use for XML-RPC calls
    """
    try:
        client = erppeek.Client(server, db=db, user=user, password=password,
                                verbose=False)
    except:
        raise RuntimeError(
            "Error connecting to {0} on {1} using credentials {2}:{3}".format(
                db, server, user, password
            )
        )
    return client


class ReallocateUsersToWards(object):
    """
    Reallocate users belonging to groups whose users are assigned to wards.

    Such groups are stored in a class attribute, to be easily referenced from
    inside the class' methods.
    """

    def __init__(self, server, db, user='admin', password='admin'):
        self.user_model = 'res.users'
        self.groups_model = 'res.groups'
        self.user_management = 'nh.clinical.user.management'
        self.client = get_erppeek_client(server=server, db=db, user=user,
                                         password=password)
        resp_model = 'nh.clinical.user.responsibility.allocation'
        self.resp = self.client.model(resp_model)
        self.groups_list = [
            'NH Clinical Senior Manager Group',
            'NH Clinical Ward Manager Group',
            'NH Clinical Doctor Group',
        ]

    def reallocate_users_by_group(self, group_name):
        """
        Reallocate users belonging to a specific group, passed as argument.

        :param group_name: name of the group
        :type group_name: str
        """
        group = self.client.search(
            self.groups_model, [['name', '=', group_name]]
        )
        users = self.client.search(
            self.user_model,
            [
                ['pos_id', '!=', None],
                ['groups_id', 'in', group]
            ]
        )
        for user in users:
            current_data = self.client.read(self.user_management,
                                           user, ['ward_ids'])['ward_ids']
            resp_act = self.resp.create_activity({}, {
                'responsible_user_id': user,
                'location_ids': [[6, False, current_data]]
            })
            self.resp.complete(resp_act)

    def reallocate_all_users(self):
        for group in self.groups_list:
            self.reallocate_users_by_group(group)
