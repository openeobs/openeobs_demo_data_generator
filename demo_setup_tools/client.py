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
            client = erppeek.Client(server, db=db, user=user,
                                    password=password, verbose=False)
        except:
            raise RuntimeError(
                "Error connecting to {0} on {1} "
                "using credentials {2}:{3}".format(db, server, user, password)
            )
        return client

