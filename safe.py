import sqlite3
from hashlib import sha256
from safe_serialize import Master
import json
import os

# try to store this in hidden place eg:(variable environement)
Master_password = os.environ.get('master_key')

connect = input('Give me your Master Password to unlock your safe\n : ')

while connect != Master_password:
    connect = input('Give me your Master Password to unlock your safe\n : ')
    if connect == 'q':
        break

my_safe = sqlite3.connect('database.db')


def create_password(passw_key, service_name, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service_name.lower().encode('utf-8') + passw_key.encode('utf-8')).hexdigest()[:20]


def get_hex_key(admin_pass, service_name):
    return sha256(admin_pass.encode('utf-8') + service_name.lower().encode('utf-8')).hexdigest()


def get_password(admin_pass, service_name):
    secret_key = get_hex_key(admin_pass, service_name)
    service_name = service_name

    # table keys/ service name  are  created below
    cursor = my_safe.execute(
        "SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"' +
        "and S_NAMES WHERE NAME=" + '"' + service_name)

    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_password(file_string, service_name, admin_pass)


def add_password(service_name, admin_pass):
    secret_key = get_hex_key(admin_pass, service_name)
    service_name = service_name

    key_command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' % (
        '"' + secret_key + '"')
    service_command = 'INSERT INTO S_NAMES (NAME) VALUES (%s);' % (
        '"' + service_name + '"'
    )
    # execute SQL statements for the tables created
    my_safe.execute(key_command)
    my_safe.execute(service_command)
    my_safe.commit()
    return create_password(secret_key, service_name, admin_pass)


# Creating the safe_db / or if already exists return these methods above
if connect == Master_password:
    try:
        # Table Keys created
        my_safe.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')

        #  table Service_names created
        my_safe.execute(''' CREATE TABLE S_NAMES
                    (NAME TEXT NOT NULL);''')

        print(
            "\n Your safe has been created!\n --What would you like to store in it today?")
    except:
        print("You have a safe, what would you like to do today?")

    while True:
        print("\n" + "*"*15)
        print("Commands:")
        print("q = quit program")
        print("gp = get password")
        print("sp = store password")
        print("*"*15)
        input_ = input(":")

        if input_ == "q":
            break
        if input_ == "sp":
            service = input(
                "What is the name of the service you would like to Store ?\n")
            print("\n" + service.capitalize() + " password created:\n" +
                  add_password(service, Master_password))
        if input_ == "gp":
            service = input(
                "What is the name of the service you would like to GET ?\n")
            print("\n" + service.capitalize() + " password:\n" +
                  get_password(Master_password, service))

        # creating the data here
        # counter = 0
        # s_name = ''
        # service_password = ''
        # data = []
        # try:
        #     s_name = service
        #     # will retrieve the password in json file for easy access
        #     service_password = get_password()
        # except:
        #     Exception()
        # Store = Master(s_name, service_password)
        # if Store:
        #     data.append(Store)
        # counter = counter + 1

        # decode = MasterEncoder().encode(data)
        # print('Json decode  :\n', decode)

        # # Creating json file / Keep this file
        # with open('Data.json', 'w') as write_in:
        #     json_data = {}
        #     json_data['Info'] = []
        #     for i in data:
        #         json_data['Info'].append(i.serialize())
        #     json.dump(json_data, write_in, indent=4)
