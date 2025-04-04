import io
import requests

url = 'http://localhost:8001/validate'
headers = {'Accept': 'application/n-triples'}

# Providing both data and shapes:

# See: https://requests.readthedocs.io/en/latest/api/#requests.request
files = {
    'data':   ('val_ok_data.ttl',   open('tests/data/val_ok_data.ttl', 'rb'),   'text/turtle'),
    'shapes': ('val_ok_shapes.ttl', open('tests/data/val_ok_shapes.ttl', 'rb'), 'text/turtle'),
}

resp = requests.post(url=url, files=files, headers=headers)

# Validating input data with default server shapes:

data_file = {
    'data':   ('val_ok_data.ttl',   open('tests/data/val_ok_data.ttl', 'rb'),   'text/turtle'),
}
resp = requests.post(url=url, files=data_file, headers=headers)


# Using in-memory data instead of files:

data = {
    'data': (
        'demo.nt',
        io.BytesIO(b"<http://ex/1> <http://ex/2> <http://ex/3> ."),
        'application/n-triples'
    )
}

resp = requests.post(url=url, files=data, headers=headers)
