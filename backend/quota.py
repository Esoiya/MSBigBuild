import subprocess
import json
import os
import requests
import argparse

PATH_FOR_JSON = '/etc/quota'
QUOTA_JSON_FILENAME = 'users_quota.json'
FLASK_PORT = 8889
USERS_ENDPOINT = '/employees'

def get_rag_of_user(username:str, user_data:list):
    return_dict = {'used_percentage': 0, 'free_percentage': 0, 'used_megabytes': 0, 'rag': 'g'}
    if len(user_data) != 0 and user_data[0] == username:
        limit = int(user_data[4])
        return_dict['used_megabytes'] = round(int(user_data[2]) / 1024, 3)
        if limit == 0:
            return_dict['used_percentage'] = 0
            return_dict['free_percentage'] = 100
        else:
            if int(user_data[2]) > int(user_data[3]): return_dict['rag'] = 'r' 
            return_dict['used_percentage'] = round(int(user_data[2]) * 100 / limit, 3)
            return_dict['free_percentage'] = 100 - return_dict['used_percentage']
    else:
        return 'Not a valid user'
    return return_dict

def get_storage_of_user(username: str):
    p = subprocess.run(f'repquota -u /mnt/homes/ | grep {username}', stdout=subprocess.PIPE, shell=True)
    user_data = p.stdout.decode().split()

    return get_rag_of_user(username, user_data)

def get_storage_of_all():
    return_dict = {}
    p = subprocess.run(f'repquota -u /mnt/homes/', stdout=subprocess.PIPE, shell=True)
    users_list = p.stdout.decode().splitlines()
    for line in users_list[5:-2]:
        user_data = line.split()
        username = user_data[0]
        return_dict[username] = get_rag_of_user(username, user_data)

    return return_dict

def create_quota_json():
    if os.path.isdir(PATH_FOR_JSON) == False:
        os.makedirs(PATH_FOR_JSON)

    quota_file = os.path.join(PATH_FOR_JSON, QUOTA_JSON_FILENAME)

    if os.path.isfile(quota_file) == False:
        users_list = requests.get(f'http://127.0.0.1:{FLASK_PORT}/{USERS_ENDPOINT}').json()
        quota_dict = {}
        for user in users_list:
            quota_dict[user['login_id']] = {'soft_limit': 90, 'hard_limit': 100}

        with open(quota_file, 'w') as quota_json:
            quota_json.write(json.dumps(quota_dict))


def set_quota_for_user(username: str, soft_limit:int, hard_limit:int):
    quota_file = os.path.join(PATH_FOR_JSON, QUOTA_JSON_FILENAME)

    if os.path.isfile(quota_file) == False:
        create_quota_json()

    f = open(quota_file, 'r')
    quota_data = json.load(f)
    f.close()
    quota_data[username] = {'soft_limit': soft_limit, 'hard_limit': hard_limit}

    with open(quota_file, 'w') as quota_json:
        quota_json.write(json.dumps(quota_data))


def apply_quota_for_user(username:str):
    quota_file = os.path.join(PATH_FOR_JSON, QUOTA_JSON_FILENAME)

    if os.path.isfile(quota_file) == False:
        create_quota_json()
    with open(quota_file, 'r') as f:
        quota_data = json.load(f)
        soft_limit = quota_data[username]['soft_limit']
        hard_limit = quota_data[username]['hard_limit']
        p = subprocess.run(f'setquota -u {username} {soft_limit}M {hard_limit}M 0 0 /mnt/homes', stdout=subprocess.PIPE, shell=True)
        print(p.returncode)

def get_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--username', type=str, help='Username to apply quota')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    if args.username:
        apply_quota_for_user(args.username)
    print(get_storage_of_all())
    print(get_storage_of_user('tapusera'))
    print(get_storage_of_user('tapu'))
    create_quota_json()
    set_quota_for_user('alynn', 100, 120)