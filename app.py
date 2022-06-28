from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import requests
import os, sys
from datetime import datetime, timedelta
from dateutil.parser import parse
from pprint import pprint


prod=False

if prod:
    mb_bearer = os.getenv('mb_bearer')
    mb_administration = os.getenv('mb_administration')
else:
    mb_bearer = os.getenv('schaduw_mb_bearer')
    mb_administration = os.getenv('schaduw_mb_administration')



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def mb_connect(method, endpoint):
    ref = False
    headers = {}
    headers['Content-Type'] = "application/json"
    headers['Authorization'] = "Bearer {}".format(mb_bearer)
    base_url = "https://moneybird.com/api/v2/{}".format(mb_administration)
    url = "{}/{}".format(base_url, endpoint)

    if method == "GET":
        r = requests.get(url, headers=headers)
        if r and r.ok and r.json:
            ref = r.json()

    if method == "DELETE":
        r = requests.delete(url, headers=headers)
        if r and r.ok:
            ref = r.ok

    return ref


    
def tijd(description, username, projectname, contactname, start, end):
    user_id = False
    project_id = False
    contact_id = False
    started_at = False
    ended_at = False

    users = mb_connect('GET', 'users.json')
    if users:
        print("users".format())
        for user in users:
            if user['name'] == username:
                user_id = user['id']
                print("{}{} {} {}".format(bcolors.OKGREEN, user['id'], user['name'], bcolors.ENDC))
            else:
                print("{} {}".format(user['id'], user['name']))


    projects = mb_connect('GET', 'projects.json')
    if projects:
        print("\nprojects".format())
        for project in projects:
            if project['name'] == projectname:
                project_id = project['id']
                print("{}{} {} {}".format(bcolors.OKGREEN, project['id'], project['name'], bcolors.ENDC))
            else:
                print("{} {}".format(project['id'], project['name']))


    contacts = mb_connect('GET', 'contacts.json')
    if contacts:
        print("\ncontacts".format())
        for contact in contacts:
            if contact['firstname'] == contactname:
                contact_id = contact['id']
                print("{}{} {} {}{}".format(bcolors.OKGREEN, contact['id'], contact['firstname'], contact['lastname'], bcolors.ENDC))
            else:
                print("{} {} {}".format(contact['id'], contact['firstname'], contact['lastname']))

    started_at = parse(start)
    ended_at = parse(end)



    if description and user_id and project_id and contact_id and started_at and ended_at:
        print('python app tijd "{}" {} {} {} "{}" "{}"'.format(description, user_id, project_id, contact_id, started_at, ended_at))
        tijdschrijven(description, user_id, project_id, contact_id, started_at, ended_at)
    else:
        print('Niet alles gevonden')



def tijdschrijven(description, user_id, project_id, contact_id, started_at, ended_at):

    headers = {}
    headers['Content-Type'] = "application/json"
    headers['Authorization'] = "Bearer {}".format(mb_bearer)

    d = {}
    d['time_entry'] = {}
    d['time_entry']['description'] = description
    d['time_entry']['user_id'] = user_id
    d['time_entry']['project_id'] = project_id
    d['time_entry']['contact_id'] = contact_id
    d['time_entry']['started_at'] = str(started_at)
    d['time_entry']['ended_at'] = str(ended_at)
    pprint(d)


    base_url = "https://moneybird.com/api/v2/{}".format(mb_administration)
    url = "{}/{}".format(base_url, 'time_entries')
    r = requests.post(url, headers=headers, json=d)

    if r and r.ok and r.json:
        pprint(r.json())
    else:
        pprint(vars(r))


def dev():
    print('dev')


if __name__ == '__main__':
    args = sys.argv[1:]
    if 'api' in args:
        print('python app.py api method endpoint')
        print('python app.py api GET contacts.json')
        print('python app.py api DELETE time_entries/358440828513814525')
        if len(args) == 3:
            pprint(mb_connect(args[1], args[2]))

    if 'tijd' in args:
        print('example')
        print("python app tijd <omschrijving> <user_id> <project_id> <contact_id> <started_at> <ended_at>")
        now = datetime.now().isoformat(' ', 'seconds')
        print('python app.py tijd "stucen" "Ferry Schuller" Heutsz Andrzej "{0} GMT-2" "{0} GMT-2"\n'.format(now))
        if len(args) == 7:
            tijd(description=args[1], username=args[2], projectname=args[3], contactname=args[4], start=args[5], end=args[6])

    if 'dev' in args:
        pprint(args)
        dev()
