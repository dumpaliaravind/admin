# -*- coding: utf-8 -*-
import urllib, urllib2, json, ssl, socket, sys, inspect, os
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

# Set ciphers and ssl settings
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
ctx.set_ciphers('HIGH:!DH:!aNULL')

# Set proxy settings
proxy = urllib2.ProxyHandler({'https':'atlproxy.tvlport.com:443', 'http':'atlproxy.tvlport.com:8080'})
opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), proxy)
urllib2.install_opener(opener)

def get_licenses_for_api(token, apiVersionId):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiVersionId (string) - Version id for API.
    OUTPUT  1. (json) - List of licenses for API.
    '''
    licensesUrl = 'https://{}/api/apis/versions/{}/licenses'.format(endpoint, apiVersionId)
    licensesHeaders = {'Accept':'application/json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=licensesUrl, headers=licensesHeaders)
        return json.loads(urllib2.urlopen(request).read())
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def add_licenses(token, licenseData):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. licenseData (json) - Data used to add new license
    OUTPUT  1. addLicenseResp (int) – HTTP response code from request.
            2. addLicenseContent (json) - Information about the license including the unique LicenseID.
    '''
    addLicensesUrl = 'https://{}/api/licenses'.format(endpoint)
    addLicensesHeaders = {'Accept':'application/json', 'Content-Type':'application/json; charset=UTF-8', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=addLicensesUrl, headers=addLicensesHeaders, data=licenseData)
        postAddLicense = urllib2.urlopen(request)
        addLicenseResp = postAddLicense.getcode()
        addLicenseContent = postAddLicense.read()
        return addLicenseResp, json.loads(addLicenseContent)
        return urllib2.urlopen(request).getcode()
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def get_resources_for_api(token, apiVersionId):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiVersionId (string) - Version id for API.
    OUTPUT  1. (json) - Resource info for API.
    '''
    resourcesUrl = 'https://{}/api/apis/versions/{}/resources'.format(endpoint, apiVersionId)
    resourcesHeaders = {'Accept':'application/json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=resourcesUrl, headers=resourcesHeaders)
        return json.loads(urllib2.urlopen(request).read())
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def get_scopes_for_api(token, apiVersionId):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiVersionId (string) - Version id for API.
    OUTPUT  1. (json) - Scope info for API.
    '''
    scopesUrl = 'https://{}/api/apis/versions/{}/scope'.format(endpoint, apiVersionId)
    scopesHeaders = {'Accept':'application/json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=scopesUrl, headers=scopesHeaders)
        return json.loads(urllib2.urlopen(request).read())
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def get_private_viewer_scopes_for_api(token, apiVersionId, viewerId):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiVersionId (string) - Version id for API.
            3. viewerId (string) - GroupID of a group that has visibility into the API.
    OUTPUT  1. (json) - Private viewer scope for API.
    '''
    privateScopesUrl = 'https://{}/api/apis/versions/{}/viewers/{}/scope'.format(endpoint, apiVersionId, viewerId)
    privateScopesHeaders = {'Accept':'application/json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=privateScopesUrl, headers=privateScopesHeaders)
        return json.loads(urllib2.urlopen(request).read())
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def add_scope(token, businessId, scopeData):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. businessId (string) - Unique ID for a specific business organization on the platform.
            3. scopeData (json) - Data used to add new Scope.
    OUTPUT  1. addScopeResp (int) – HTTP response code from request
            2. addScopeContent (json) - Information about the scope that was added.
    '''
    addScopeUrl = 'https://{}/api/businesses/{}/resources'.format(endpoint, businessId)
    addScopeHeaders = {'Accept':'application/json', 'Content-Type':'application/json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=addScopeUrl, headers=addScopeHeaders, data=scopeData)
        postAddScope = urllib2.urlopen(request)
        addScopeResp = postAddScope.getcode()
        addScopeContent = postAddScope.read()
        return addScopeResp, json.loads(addScopeContent)
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def add_scope_mapping_to_api(token, apiVersionId, scopeMappingData):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiVersionId (string) - Version id for API.
            3. scopeMappingData (json) - Data used for scope mapping to API.
    OUTPUT  1. addScopeMappingResp (int) – HTTP response code from request
            2. addScopeMappingContent (json) - Information about the operation-specific scope mapping for the specified API version.
    '''
    addScopeMappingUrl = 'https://{}/api/apis/versions/{}/resources'.format(endpoint, apiVersionId)
    addScopeMappingHeaders = {'Accept':'application/json, text/javascript, */*; q=0.01', 'Content-Type':'application/json; charset=UTF-8', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=addScopeMappingUrl, headers=addScopeMappingHeaders, data=scopeMappingData)
        request.get_method = lambda: 'PUT'
        putAddScopeMapping = urllib2.urlopen(request)
        addScopeMappingResp = putAddScopeMapping.getcode()
        addScopeMappingContent = putAddScopeMapping.read()
        return addScopeMappingResp, json.loads(addScopeMappingContent)
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False
