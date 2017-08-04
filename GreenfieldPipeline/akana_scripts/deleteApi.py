# -*- coding: utf-8 -*-
import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re, inspect
from tools.format import readable_json
from tools.auth_token import get_csrf_token
from tools.apis import delete_api_version, delete_api, get_api_info, get_apis_list


# Check and set host environment variable
pipelineEnv = os.environ.get('ENVIRONMENT')
endpoint, pm_env = None, None

if pipelineEnv == None:
    pm_env = socket.gethostname()[3:5]
else:
    if pipelineEnv not in ['dv', 'pp', 'pn']:
        print 'Error: Pipeline environment varialble incorrect.  Place correct environment variables in pipeline script.  Options: dv, pp, pn.'
        exit()
    else:
        pm_env = pipelineEnv


# Get csrf token
csrfToken = get_csrf_token(os.environ.get('Akanauser'), os.environ.get('Akanapass'))


# Get API version id
targetName = os.environ.get('APINAME')
apiList = get_apis_list(csrfToken)
apiId = None
for api in range(len(apiList)):
    apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
    if apiInfo['Name'] == targetName:
        apiId = apiInfo['APIID']


# Delete API
if apiId != None:
    deleteApiResp = delete_api(csrfToken, apiId)

    if deleteApiResp == 200:
        print 'API deleted successfully.'
    else:
        print 'Error: API deletion failed.'
else:
    print 'Error: Unable to find API based on provided name for deletion.  Please recheck name variable in pipeline script.'
