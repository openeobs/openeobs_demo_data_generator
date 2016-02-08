import csv


class UserCSVWriter(object):

    fieldnames = ['user_id', 'username', 'System Administrator', 'Kiosk',
                  'Senior Manager', 'Receptionist', 'Doctor', 'Senior Doctor',
                  'Junior Doctor', 'Registrar', 'Consultant', 'Ward Manager',
                  'Nurse', 'HCA']

    def __init__(self, filename, users):
        users.insert(0, self.fieldnames)
        with open(filename, 'wb') as csv_output_file:
            writer = csv.writer(csv_output_file)
            writer.writerows(users)

