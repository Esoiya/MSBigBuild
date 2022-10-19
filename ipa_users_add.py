import json
import requests
import urllib3
import os
import subprocess

from python_freeipa import ClientMeta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

newUserJson = requests.get('http://94.237.60.14:8889/employees').json()

client = ClientMeta('ipaserver3.ee-bb.test', verify_ssl=False)
client.login('admin', 'pinkEleph@nt!')


kerb_users = []
ipaUserJson = client.user_find()
for i in range(len(ipaUserJson['result'])):
  kerb_users.append(ipaUserJson['result'][i]['uid'])


for employee in newUserJson:
  if employee['login_id'] not in kerb_users:
    fname, lname = employee['name'].split(' ')
    home_dir = '/mnt/homes/' + login_id
    subprocess.run(["mkdir", home_dir])
    subprocess.run(["chown", login_id, home_dir])
    client.user_add(employee['login_id'], employee['fname'], employee['lname'], /
    employee['name'], o_homedirectory=home_dir, o_loginshell='/bin/bash', o_ou=employee['dept_id'])
    subprocess.run(["setquota", "-u", login_id, "80M", "100M", "0", "0", home_dir])
