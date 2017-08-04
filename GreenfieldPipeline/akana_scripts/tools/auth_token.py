# -*- coding: utf-8 -*-
import urllib, urllib2, ssl, cookielib, json, socket, sys, inspect, os
from tools.format import readable_json

# Check and set host environment variable
pipelineEnv = os.environ.get('ENVIRONMENT')
endpoint, pm_env = None, None

if pipelineEnv == None:
    pm_env = socket.gethostname()[3:5]
else:
    if pipelineEnv not in ['dv', 'pp', 'pn']:
        print('Pipeline environment varialble incorrect.  Place correct environment variables in pipeline script.  Options: dv, pp, pn.')
        exit()
    else:
        pm_env = pipelineEnv

if(pm_env == 'dv'):
    endpoint = 'apiportal.dv.tvlport.com'
elif(pm_env == 'pp'):
    endpoint = 'apiportal.pp.tvlport.com'
elif(pm_env == 'pn'):
    endpoint = 'apiportal.travelport.com'
else:
    endpoint = 'apiportal.pp.tvlport.com'   # Default to PP when testing locally

def get_csrf_token(username, password):
    '''
    INPUT   1. username (string) - Account username.
            2. password (string) - Account password.
    OUTPUT  1. (string) – Cross site request forgery token used to make rest calls to Akana API.
    '''
    cookieJar = cookielib.CookieJar()

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_ciphers('HIGH:!DH:!aNULL')

    proxy = urllib2.ProxyHandler({'https':'atlproxy.tvlport.com:443', 'http':'atlproxy.tvlport.com:8080'})
    opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), urllib2.HTTPCookieProcessor(cookieJar), proxy)
    urllib2.install_opener(opener)

    loginUrl = 'https://{}/api/login/ssoLogin'.format(endpoint)
    loginHeaders = {'Accept':'application/json', 'Content-Type':'application/x-www-form-urlencoded'}
    loginPayload = {
        'domain':'Travelport AD',
        'identity_username':username,
        'secret_password':password
    }
    loginPayloadData = urllib.urlencode(loginPayload)
    
    try:
        request = urllib2.Request(url=loginUrl, headers=loginHeaders, data=loginPayloadData)
        loginResponse = urllib2.urlopen(request)
        cookieData = dict((cookie.name, cookie.value) for cookie in cookieJar)
        return cookieData['Csrf-Token_travelportAPI']
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def get_csrf_token_with_email(email, password):
    '''
    INPUT   1. email (string) - Account email address.
            2. password (string) - Account password.
    OUTPUT  1. (string) – Cross site request forgery token used to make rest calls to Akana API.
    '''
    cookieJar = cookielib.CookieJar()

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_ciphers('HIGH:!DH:!aNULL')

    proxy = urllib2.ProxyHandler({'https':'atlproxy.tvlport.com:443', 'http':'atlproxy.tvlport.com:8080'})
    opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), urllib2.HTTPCookieProcessor(cookieJar), proxy)
    urllib2.install_opener(opener)

    loginUrl = 'https://{}/api/login'.format(endpoint)
    loginHeaders = {'Accept':'application/json, text/javascript, */*; q=0.01', 'Content-Type':'application/json; charset=UTF-8'}

    loginCredBody = {
        "email":email,
        "password":password
    }
    loginCredBody = json.dumps(loginCredBody)

    try:
        request = urllib2.Request(url=loginUrl, headers=loginHeaders, data=loginCredBody)
        request.get_method = lambda: 'POST'
        loginResponse = urllib2.urlopen(request)
        cookieData = dict((cookie.name, cookie.value) for cookie in cookieJar)
        return cookieData['Csrf-Token_travelportAPI']
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False
    
