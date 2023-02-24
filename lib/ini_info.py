from lib.config_r import readini

env = readini('env.ini').readr('venv')['env']
if env == 0:
    # product
    venv = False
else:
    # development
    venv = True


def blue_print_info():
    return readini('blueprint.ini').readr('blue-print')


def DB_INFO():
    return readini().readr()


def get_info():
    token_info = readini('access.ini').readr('access_token')
    issuer = token_info['issuer']
    key = token_info['key']
    expiration_time = int(token_info['expiration_time'])

    return issuer, key, expiration_time


def upload_host():
    res = readini('host.ini').readr('host')
    if venv == 1:
        host_domain = res['venv_domain']
    else:
        host_domain = res['domain']
    return host_domain


def ase_info():
    res = readini('aes.ini').readr('aes')
    iv = res['iv']
    key = res['key']

    return key, iv


def public_str():
    res = readini('env.ini').readr('public_str')
    return res
