from python_freeipa import ClientMeta
import json
import requests

req = requests.get('http://94.237.60.14:8889/employees')
print(req.json())

# client = ClientMeta('ipaserver3.ee-bb.test')
# client.login('admin', 'pinkEleph@nt!')
# user = client.user_add()