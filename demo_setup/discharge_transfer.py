import erppeek

def database_connect(host, db, user):
    """Connect to the database"""
    try:
        client = erppeek.Client(host, db=db, user=user, password=user, verbose=False)
        assert client
    except:
        raise RuntimeError('Something failed!')
    return client

def discharge_patient(client):
    api_demo = client.model('nh.eobs.demo.loader')
    api_demo.discharge_patients('A', 1)

def transfer_patient(client):
    api_demo = client.model('nh.eobs.demo.loader')
    api_demo.transfer_patients('B', 'A', 1)

client = database_connect('http://localhost:8069', 'demo_data_master', 'winifred')
#discharge_patient(client)
#transfer_patient(client)
