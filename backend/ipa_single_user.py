import json
import requests
import urllib3
import os
import subprocess
from quota import *

from python_freeipa import ClientMeta

def ipa_add_user(login_id, name, dept_id, onboarded):
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

  client = ClientMeta('ipaserver3.ee-bb.test', verify_ssl=False)
  client.login('admin', 'pinkEleph@nt!')

  fname, lname = (name.rstrip()).split(' ')
  full_name = name.rstrip()
  home_dir = os.path.join('/mnt/homes/', login_id)
  subprocess.run(["mkdir", home_dir])
  subprocess.run(["chmod", "775", home_dir])
  client.user_add(login_id, fname, lname, \
  full_name, o_homedirectory=home_dir, o_loginshell='/bin/bash', o_ou=dept_id, \
  o_userpassword="TempPass")
  subprocess.run(["chown", login_id, home_dir])
  set_quota_for_user(login_id, 80, 100)