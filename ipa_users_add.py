import json
import requests
import urllib3
import os
import subprocess
from backend.quota import *

from python_freeipa import ClientMeta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

newUserJson = requests.get('http://94.237.60.14:8889/employees').json()

client = ClientMeta('ipaserver3.ee-bb.test', verify_ssl=False)
client.login('admin', 'pinkEleph@nt!')

kerb_users = []
ipaUserJson = client.user_find()
for i in range(len(ipaUserJson['result'])):
  kerb_users.append(str(ipaUserJson['result'][i]['uid'][0]))

for employee in newUserJson:
  if employee['login_id'] not in kerb_users:
    fname, lname = (employee['name'].rstrip()).split(' ')
    full_name = employee['name'].rstrip()
    home_dir = os.path.join('/mnt/homes/', employee['login_id'])
    subprocess.run(["mkdir", home_dir])
    subprocess.run(["chmod", "775", home_dir])
    client.user_add(employee['login_id'], fname, lname, \
    full_name, o_homedirectory=home_dir, o_loginshell='/bin/bash', o_ou=employee['dept_id'], \
    o_userpassword="TempPass")
    subprocess.run(["chown", employee['login_id'], home_dir])
    set_quota_for_user(employee['login_id'], 80, 100)