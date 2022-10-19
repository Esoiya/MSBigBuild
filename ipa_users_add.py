import json
import requests
import urllib3

from python_freeipa import ClientMeta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#req = requests.get('http://94.237.60.14:8889/employees').json()

client = ClientMeta('ipaserver3.ee-bb.test', verify_ssl=False)
client.login('admin', 'pinkEleph@nt!')

print(client.user_find())
# user = client.user_add()