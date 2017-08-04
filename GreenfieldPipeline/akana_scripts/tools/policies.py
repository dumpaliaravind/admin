# -*- coding: utf-8 -*-
import urllib, urllib2, json, ssl, socket, sys, inspect, os

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

# Set ciphers and ssl settings
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
ctx.set_ciphers('HIGH:!DH:!aNULL')

# Set proxy settings
proxy = urllib2.ProxyHandler({'https':'atlproxy.tvlport.com:443', 'http':'atlproxy.tvlport.com:8080'})
opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), proxy)
urllib2.install_opener(opener)

def get_policies_list(token):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
    OUTPUT  1. (list) - List of all policies.
    '''
    policiesListUrl = 'https://{}/api/policies'.format(endpoint)
    policiesListHeaders = {'Accept':'application/json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=policiesListUrl, headers=policiesListHeaders)
        getPoliciesListResponse = json.loads(urllib2.urlopen(request).read())

        policiesList = []
        for policy in range(len(getPoliciesListResponse['channel']['item'])):
            policiesList.append(getPoliciesListResponse['channel']['item'][policy])
        return policiesList
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def attach_policy_to_api(token, rawData, apiVersionId, implementation):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. rawData (json) - Data used to attach policy to API.
            3. apiVersionId (string) - Version id of API.
            4. implementation (string) - Implementation environment, either 'live' or 'sandbox'.
    OUTPUT  1. (json) - Updated policy information for the API version implementation.
    '''
    attachPolicyToApiUrl = 'https://{}/api/apis/versions/{}/implementations/{}/policies'.format(endpoint, apiVersionId, implementation)
    attachPolicytoApiHeaders = {'Accept':'application/vnd.soa.v81+json', 'Content-Type':'application/vnd.soa.v81+json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=attachPolicyToApiUrl, headers=attachPolicytoApiHeaders, data=rawData)
        request.get_method = lambda: 'PUT'
        return urllib2.urlopen(request).getcode()
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def policy_attach_format(policy):
    '''
    INPUT   1. policy (json) - Policy to be formatted.
    OUTPUT  1. (json) - Formatted policy.
    '''
    return {
        "PolicyKey": policy['guid']['value'],
        "Name": policy['title'],
        "Description": policy['description'],
        "PolicyType": policy['category'][1]['value'],
        "PolicySubType": policy['category'][0]['value']
    }

    