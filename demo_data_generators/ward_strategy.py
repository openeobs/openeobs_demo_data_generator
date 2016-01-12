# coding=utf-8
import re


class Patient(object):

    def __init__(self):
        self.id = None
        self.patient_id = None
        self.placement_id = None
        self.activity_id = None
        self.spell_activity_id = None
        self.date_terminated = None

    def set_id(self):
        match = re.search('(\d+)$', self.patient_id)
        if match is not None:
            self.id = match.group()


class WardStrategy(object):

    def __init__(self, patients, risk_distribution, partial_news_per_patient):
        self.patients = patients
        self.risk_distribution = risk_distribution
        self.partial_news_per_patient = partial_news_per_patient


def patients_factory(root):
    """Returns a list of patients."""

    placements = root.findall(
            ".//record/[@model='nh.clinical.patient.placement']"
    )
    patients = []

    for placement in placements:
        patient = patient_factory(placement, root)
        patients.append(patient)

    return patients


def patient_factory(placement, root):
    """Creates a patient."""

    patient = Patient()
    patient.placement_id = placement.attrib['id']

    for field in placement:
        # append acitivty_id
        if field.attrib['name'] == "activity_id":
            patient.activity_id = field.attrib['ref']

            # search corresponding activity
            search_string = ".//record/[@id='%s']" % field.attrib['ref']
            activity_records = root.findall(search_string)
            for activity_record in activity_records:

                for field in activity_record:
                    # get spell_activity_id
                    if field.attrib['name'] == 'spell_activity_id':
                         patient.spell_activity_id = field.attrib['ref']

                    # get date_terminated
                    if field.attrib['name'] == 'date_terminated':
                        patient.date_terminated = field.attrib['eval']

        # append patient_id
        if field.attrib['name'] == 'patient_id':
            patient.patient_id = field.attrib['ref']

        # append location_id (bed)
        if field.attrib['name'] == 'location_id':
            patient.location_id = field.attrib['ref']

    patient.set_id()
    return patient

