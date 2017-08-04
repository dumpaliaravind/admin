import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os
from tools.auth_token import get_csrf_token
from tools.format import readable_json
from tools.apis import add_doc_to_api, get_apis_list, get_api_info

targetName = os.environ.get('APINAME')
zipFilePath = 'test_files/test_files.zip' 
htmlFilePath = 'test_files/sample.html' 

# Get csrf token
csrfToken = get_csrf_token(os.environ.get('Akanauser'), os.environ.get('Akanapass'))

apiList = get_apis_list(csrfToken)

# Get APIID of target API
apiId = None
for api in range(len(apiList)):
    apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
    if apiInfo['Name'] == targetName:
        apiId = apiInfo['APIID']

# Add zip file to API
addZipFileResp = add_doc_to_api(csrfToken, zipFilePath, id=apiId)
if addZipFileResp == 200:
    print 'Zip file added to API successfully.'
else:
    print 'Zip file addition to API failed.'

# Add html file to API
addHtmlFileResp = add_doc_to_api(csrfToken, htmlFilePath, id=apiId)
if addHtmlFileResp == 200:
    print 'HTML file added to API successfully.'
else:
    print 'HTML file addition to API failed.'