# Using http://docs.python-requests.org/ to access OMERO via json api.
# Url docs at:
# http://downloads.openmicroscopy.org/omero/5.2.4/api/python/omeroweb/omeroweb.webgateway.html#module-omeroweb.webgateway.urls

import requests
import getpass
from omeroidr.constants import API_LOGIN, API_LOGOUT

def connect_to_omero(base_url: str, user: str, password: str):

    session = requests.Session()

    login_url = base_url + API_LOGIN
    session.get(login_url)
    token = session.cookies['csrftoken']

    if (user == None):
        user = input('OMERO Username (return for public repository): ')

    if (password == None):
        password = getpass.getpass('OMERO Password (return for public repository): ')

    # Login with username, password and server
    payload = {'username': user,
           'password': password,
           'server': 1,
           'noredirect': 1,
           'csrfmiddlewaretoken': token}
    r = session.post(login_url, data=payload, headers=dict(Referer=login_url))

    # Return session handle
    return session

def disconnect(session, base_url: str):
    logout_url = base_url + API_LOGOUT
    login_url = base_url + API_LOGIN
    r = session.post(logout_url, headers=dict(Referer=login_url))
