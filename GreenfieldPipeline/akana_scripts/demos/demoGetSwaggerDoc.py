import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os
from tools.apis import get_apis_list, get_api_info, get_policies_for_api, get_swagger_doc_for_api
from tools.auth_token import get_csrf_token
from tools.format import readable_json

# Get csrf token
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

apiList = get_apis_list(csrfToken)

for api in range(len(apiList)):
    apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
    swaggerDoc = get_swagger_doc_for_api(csrfToken, apiInfo['LatestVersionID'])
    print '\n\n' + readable_json(swaggerDoc)