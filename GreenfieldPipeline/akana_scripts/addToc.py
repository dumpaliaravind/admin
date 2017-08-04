import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, glob, fnmatch
from tools.auth_token import get_csrf_token
from tools.format import readable_json
from tools.apis import add_doc_to_api, get_apis_list, get_api_info
from tools.toc import generate_default_toc

targetName = os.environ.get('APINAME')

# Get csrf token
csrfToken = get_csrf_token(os.environ.get('Akanauser'), os.environ.get('Akanapass'))

apiList = get_apis_list(csrfToken)

# Get APIID of target API
apiId = None
apiVerId = None
for api in range(len(apiList)):
    apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
    if apiInfo['Name'] == targetName:
        apiId = apiInfo['APIID']
        apiVerId = apiInfo['LatestVersionID']

generate_default_toc(apiVerId)

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

# Overwrite default toc file
filePathFound = find('*.travelportAPI.json', 'apimgmt')
filePath = filePathFound[0]

jsonText = {
    "sequence":["test_files.zip"],
    "displayNames":{"test_files.zip":"Test Files"},
    "toc":["test_files.zip"],
    "defaultFile":""
}
jsonFile = open(filePath, 'w+')
jsonFile.write(json.dumps(jsonText))
jsonFile.close()

# Add zipfile to API
addFileResp = add_doc_to_api(csrfToken, filePath, id=apiId)
if addFileResp == 200:
    print 'TOC file added to API successfully.'
else:
    print 'TOC file addition to API failed.'