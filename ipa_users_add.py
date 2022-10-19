from python_freeipa import ClientMeta
import json
import requests

#req = requests.get('http://94.237.60.14:8889/employees').json()

client = ClientMeta('https://ipaserver3.ee-bb.test')
client.login('admin', 'pinkEleph@nt!')

created_users = client.user_find()

# user = client.user_add()