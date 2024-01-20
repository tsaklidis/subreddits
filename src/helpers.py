import requests
import hashlib
import datetime


# Use this helpers in order to avoid the use of PRAW
# Define your credentials

ACC = {
    'password': '',
    'username': ''
}
APP = {
    'id': '',
    'secret': ''
}


def get_token():

    base_url = 'https://www.reddit.com/'

    data = {'grant_type': 'password',
            'username': ACC['username'],
            'password': ACC['password']}

    auth = requests.auth.HTTPBasicAuth(
        APP['id'],
        APP['secret'])

    r = requests.post(base_url + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': 'subreddits by steftsak'},
                      auth=auth)

    return r.json()['access_token']


def list_subs():
    token = 'bearer ' + get_token()
    base_url = 'https://oauth.reddit.com'
    headers = {'Authorization': token, 'User-Agent': 'save-subreddits'}

    response = requests.get(
        base_url + '/subreddits/mine/subscriber.json', headers=headers)
    all_subs = []

    for sub in response.json()['data']['children']:
        all_subs.append(sub['data']['display_name'])

    return all_subs


def get_text(length=8, prefix='', suffix='', invalid_chars=False):
    '''
    Create a random string based on timestamp
    Don't overload your system over get_random_string(1000000)
    :param length: The length of the text
    :param prefix: Add the same string at the beginning of the final text
    :param suffix: Add the same string at the end of the final text
    :param invalid_chars: Exclude the given characters from the result
    :return: String
    '''
    u = ''
    if (not isinstance(length, int)) or length < 4:
        length = 8
    while True:
        if len(u) < length:
            the_moment = str(datetime.datetime.now()).encode('utf-8')
            salt = hashlib.sha256(the_moment).hexdigest().encode('utf-8')
            u += hashlib.sha1(salt).hexdigest()
        else:
            break
    if invalid_chars and isinstance(invalid_chars, str):
        for ch in invalid_chars:
            u = u.replace(ch, "")
    return f'{prefix}{u[:length]}{suffix}'


def log(msg, level='info'):
    '''
    Log a message based on level
    :param msg: The value to print
    :param level: The level message
    :return:
    '''
    if level == 'info':
        sign = '[i]'
    elif level == 'error':
        sign = '[e]'
    elif level == 'question':
        sign = '[Q]'
    else:
        sign = ''
    print(f'{sign} {msg}')