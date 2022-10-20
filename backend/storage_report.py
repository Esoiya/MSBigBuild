from genericpath import isfile
import quota
import json
import os
from datetime import datetime
import subprocess

current_date = datetime.now().strftime("%Y_%m_%d")

LOG_FILE_PATH = '/var/log/report'
LOG_FILE_NAME = f'{current_date}_storage_report.json'
EMAIL_FILE_PATH = '/etc/reporting'
EMAIL_FILE_NAME = 'emails'
MESSAGE_SUBJECT = f'Storage report {current_date}'


def check_path(path):
    if os.path.isdir(path) == False:
        os.makedirs(path)

def read_email_addresses():
    email_file = os.path.join(EMAIL_FILE_PATH, EMAIL_FILE_NAME)
    email_list = []
    if os.path.isfile(email_file):
        with open(email_file) as f:
            email_list = f.read().splitlines()
    return email_list

def create_log_file():
    log_file = os.path.join(LOG_FILE_PATH, LOG_FILE_NAME)
    with open(log_file, 'w') as f:
        f.write(json.dumps(quota.get_storage_of_all(), indent=4))

def send_reports(emails):
    log_file = os.path.join(LOG_FILE_PATH, LOG_FILE_NAME)
    create_log_file()
    email_body = subprocess.run(f'df -h', stdout=subprocess.PIPE, shell=True).stdout.decode()
    for email in emails:
        subprocess.run(f'mail -s "{MESSAGE_SUBJECT}" -a {log_file} "{email}" <<< "{email_body}"', stdout=subprocess.PIPE, shell=True)
    


check_path(LOG_FILE_PATH)
check_path(EMAIL_FILE_PATH)
emails = read_email_addresses()
send_reports(emails)
