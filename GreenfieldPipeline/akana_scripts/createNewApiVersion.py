import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re, inspect
from shutil import copyfile
from tools.format import readable_json
from tools.auth_token import get_csrf_token
from tools.apis import upload_file_to_dropbox, create_api_with_file, get_apis_list, create_api, get_api_info, add_doc_to_api, create_new_api_version


# Check and set host environment variable
pipelineEnv = os.environ.get('ENVIRONMENT')
endpoint, pm_env = None, None

if pipelineEnv == None:
    pm_env = socket.gethostname()[3:5]
else:
    if pipelineEnv not in ['dv', 'pp', 'pn']:
        print 'Error: Pipeline environment variable incorrect.  Place correct environment variables in pipeline script.  Options: dv, pp, pn.'
        exit()
    else:
        pm_env = pipelineEnv


# Get csrf token
csrfToken = get_csrf_token(os.environ.get('Akanauser'), os.environ.get('Akanapass'))


targetName = os.environ.get('APINAME')
newApiVerName = os.environ.get('NEWAPIVERNAME')
newApiVerDescription = os.environ.get('NEWAPIVERDESCRIPTION')


# Get app id/version id of target API
apiList = get_apis_list(csrfToken)
apiId = None
apiVerId = None
for api in range(len(apiList)):
    apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
    if apiInfo['Name'] == targetName:
        apiId = apiInfo['APIID']
        apiVerId = apiInfo['LatestVersionID']


createNewApiVersionResp, createNewApiVersionContent = create_new_api_version(csrfToken, apiId, newApiVerName, newApiVerDescription, apiVerId)
if createNewApiVersionResp == 200:
    print 'New API Version created successfully.'
    print 'createNewApiVersionContent = \n', readable_json(createNewApiVersionContent)
else:
    print 'New API Version creation failed.'
