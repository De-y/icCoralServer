import requests

url = 'http://localhost:3000/api/getinfo'

data = {
    'username': 'av.c',
    'authorization': 'aviance.corp$$$$$$$$23243485348&*!#%@^'
}

r = requests.post(url, json=data)
