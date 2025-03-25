import io
import requests

url = 'http://localhost:15400/validate'
headers = {'Accept': 'application/n-triples'}

# Providing both data and shapes:

# See: https://requests.readthedocs.io/en/latest/api/#requests.request
files = {
    'data':   ('data.nt',   open('data/ex/data.nt', 'rb'),   'text/turtle'),
    'shapes': ('shapes.nt', open('data/ex/shapes.nt', 'rb'), 'text/turtle'),
}

resp = requests.post(url=url, files=files, headers=headers)

# Validating input data with default server shapes:

data_file = {
    'data':   ('data.nt',   open('data/ex/data.nt', 'rb'),   'text/turtle'),
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
