import hashlib
import datetime


def get_text(length=8, prefix='', suffix='', invalid_chars=False):
    '''
    Create a random string based on timestamp
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
    if level == 'info':
        sign = '[i]'
    elif level == 'error':
        sign = '[e]'
    elif level == 'question':
        sign = '[Q]'
    elif level == 'warn':
        sign = '[!]'
    else:
        sign = ''
    print(f'{sign} {msg}')


def confirm(prompt):
    ans = input(f'    {prompt} (Y/N): ')
    return ans.strip().lower() == 'y'


def choose(prompt, options):
    labels = ' '.join(f'{v}={k}' for k, v in options.items())
    log(f'{prompt}\n    {labels}', 'question')
    ans = input('    > ').strip().lower()
    return options.get(ans.upper(), ans)
