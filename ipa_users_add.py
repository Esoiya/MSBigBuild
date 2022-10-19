from python_freeipa import ClientMeta
import json
import requests

#req = requests.get('http://94.237.60.14:8889/employees').json()

client = ClientMeta(dns_lookup=True)
client.login('admin', 'pinkEleph@nt!')

created_users = client.user_find()

# user = client.user_add()