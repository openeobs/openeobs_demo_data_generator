from demo_setup_tools.client import get_erppeek_client


class SubmitObservations(object):

    def __init__(self, server, database, user, password, days):
        client = get_erppeek_client(server=server, db=database, user=user,
                                    password=password)
        SubmitInitialObservations(client, days)

        patient_pool = client.model('nh.clinical.patient')
        patient_ids = patient_pool.search([])

        # break list of patient ids into sub-lists of length 10
        n = 10
        new_patient_ids = [patient_ids[i:i+n] for i in range(0, len(patient_ids), n)]
        # submit observation 10 patients by 10 patients
        for patients in new_patient_ids:
            SubmitFinalObservations(client, days, patients)


class SubmitInitialObservations(object):

    def __init__(self, client, days):
        self.client = client
        self.submit_observations(days)

    def submit_observations(self, days):
        api_demo = self.client.model('nh.eobs.demo.loader')
        api_demo.complete_first_ews_for_placed_patients(days)


class SubmitFinalObservations(object):

    def __init__(self, client, days, patients):
        self.client = client
        self.submit_observations(days, patients)

    def submit_observations(self, days, patients):
        api_demo = self.client.model('nh.eobs.demo.loader')
        api_demo.generate_news_simulation(days, patients)
