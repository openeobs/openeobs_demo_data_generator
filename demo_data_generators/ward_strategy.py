# coding=utf-8
import random
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

    def __init__(self, patients, user_ids, risk_distribution,
                 partial_news_per_patient):
        self.patients = patients
        self.user_ids = user_ids
        self.risk_distribution = risk_distribution
        self.partial_news_per_patient = partial_news_per_patient

    def pick_user_id(self):
        return random.choice(self.user_ids)


def patients_factory(root):
    """Returns a list of patients."""

    placements = root.findall(
        ".//record/[@model='nh.clinical.patient.placement']")
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
        # append activity_id
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


def get_hca_nurse_users(ward_users):
    """Gets the nurse and hca ids for ward."""

    users = ward_users.findall(".//record/[@model='res.users']")
    user_ids = []
    hca = "[(4, ref('nh_clinical.role_nhc_hca'))]"
    nurse = "[(4, ref('nh_clinical.role_nhc_nurse'))]"

    # get user_id if hca or nurse
    for user in users:
        user_id = user.attrib['id']
        role = get_role(user)
        if role == hca or role == nurse:
            user_ids.append(user_id)

    return user_ids


def get_role(user):
    """Gets the role of the user."""

    role = None
    for field in user:
        if field.attrib['name'] == 'category_id':
            role = field.attrib['eval']
    return role
