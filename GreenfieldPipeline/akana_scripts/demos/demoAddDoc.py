import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os
from tools.auth_token import get_csrf_token
from tools.format import readable_json
from tools.apis import add_doc_to_api, get_apis_list, get_api_info

targetName = 'jeffreys_api1_v1_live'
filePath = 'test_files/toc.74667985-41e0-4d06-b878-895c40d7f583.travelportAPI.json' # Document file path location

# Get csrf token
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

apiList = get_apis_list(csrfToken)

# Get APIID of target API
apiId = None
for api in range(len(apiList)):
    apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
    if apiInfo['Name'] == targetName:
        apiId = apiInfo['APIID']

# Add document to API
addDocResp = add_doc_to_api(csrfToken, filePath, id=apiId)
if addDocResp == 200:
    print 'Document added to API successfully.'
else:
    print 'Document addition to API failed.'