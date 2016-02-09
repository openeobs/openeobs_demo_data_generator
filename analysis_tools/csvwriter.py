import csv


def column_names():
    """Returns list of columns names for the csv file."""
    return ['user_id', 'username', 'System Administrator', 'Kiosk',
            'Senior Manager', 'Receptionist', 'Doctor', 'Senior Doctor',
            'Junior Doctor', 'Registrar', 'Consultant', 'Ward Manager',
            'Nurse', 'HCA']


def add_column_names(users):
    """Prepends the column names to a list of users."""
    users.insert(0, column_names())


def create_user_csv(filename, users):
    """Creates and writes to csv file the list of users."""
    add_column_names(users)
    with open(filename, 'wb') as csv_output_file:
            writer = csv.writer(csv_output_file)
            writer.writerows(users)
