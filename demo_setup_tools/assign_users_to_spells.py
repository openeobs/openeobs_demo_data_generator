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


class ReallocateWardManagers(object):

    def __init__(self, server, db, user='admin', password='admin'):
        client = get_erppeek_client(server=server, db=db, user=user,
                                         password=password)
        user_model = 'res.users'
        user_management = 'nh.clinical.user.management'
        groups_model = 'res.groups'
        resp_model = 'nh.clinical.user.responsibility.allocation'

        wm_group = client.search(
            groups_model, [['name', '=', 'NH Clinical Ward Manager Group']]
        )

        users = client.search(
            user_model,
            [
                ['pos_id', '!=', None],
                ['groups_id', 'in', wm_group]
            ]
        )

        resp = client.model(resp_model)
        for user in users:
            current_foo = client.read(user_management, user, ['ward_ids'])['ward_ids']
            resp_act = resp.create_activity({}, {
                'responsible_user_id': user,
                'location_ids': [[6, False, current_foo]]
            })
            resp.complete(resp_act)


ReallocateWardManagers('http://localhost:8069', 'eobs_demo_data_master', user='olga', password='olga')
