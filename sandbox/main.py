import io
from krakenio import Client

api = Client('f66cec6f44df73d3ba48d8dbce302738', '7bbd29dd53c00a068b7ebe20b074540a0d7cea9d')

data = {
    'wait': True
}

result = api.upload('sandbox/dog.jpg', data)

if result.get('success'):
    print (result.get('kraked_url'))
else:
    print (result.get('message'))