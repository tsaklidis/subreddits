import requests

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



