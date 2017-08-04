# -*- coding: utf-8 -*-
import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re, inspect
from tools.format import readable_json
from tools.auth_token import get_csrf_token
from tools.apis import delete_api_version, delete_api, get_api_info, get_apis_list, get_api_versions

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

csrfToken = get_csrf_token(os.environ.get('Akanauser'), os.environ.get('Akanapass'))
targetName = os.environ.get('APINAME')
targetVersion = os.environ.get('APIVERSION')

apiList = get_apis_list(csrfToken)

# Get API version id
apiId = None
for api in range(len(apiList)):
    apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
    if apiInfo['Name'] == targetName:
        apiId = apiInfo['APIID']

apiVersionId = None
if apiId != None:
    apiVersionInfo = get_api_versions(csrfToken, apiId)
    for api in apiVersionInfo['channel']['item']:
        if api['title'] == targetVersion:
            apiVersionId = api['guid']['value']

    deleteApiVersionResp = delete_api_version(csrfToken, apiVersionId)

    if deleteApiVersionResp == 200:
        print 'API version deleted successfully.'
    else:
        print 'Error: API version deletion failed.' 
else:
    print 'Error: Unable to find API based on provided name for deletion.  Please recheck name variable in pipeline script'


