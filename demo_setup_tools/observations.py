from demo_setup_tools.client import get_erppeek_client


class SubmitObservations(object):

    def __init__(self, server, database, user, password, days):
        client = get_erppeek_client(server=server, db=database, user=user,
                                    password=password)
        SubmitInitialObservations(client, days)
        SubmitFinalObservations(client, days)


class SubmitInitialObservations(object):

    def __init__(self, client, days):
        self.client = client
        self.submit_observations(days)

    def submit_observations(self, days):
        api_demo = self.client.model('nh.eobs.demo.loader')
        api_demo.complete_first_ews_for_placed_patients(days)


class SubmitFinalObservations(object):

    def __init__(self, client, days):
        self.client = client
        self.submit_observations(days)

    def submit_observations(self, days):
        api_demo = self.client.model('nh.eobs.demo.loader')
        api_demo.generate_news_simulation(days)
