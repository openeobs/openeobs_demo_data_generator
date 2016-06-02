class DummyPatient:
    def __init__(self, hospitalnumber, patient_identifier, family_name, given_name, sex=None, dob=None, pos=None,
                 location_code=None, start_date=None):
        self.hospitalnumber = hospitalnumber
        self.patient_identifier = patient_identifier
        self.family_name = family_name
        self.given_name = given_name
        self.sex = sex
        self.dob = dob
        self.POS = pos
        self.location = location_code
        self.start_date = start_date
