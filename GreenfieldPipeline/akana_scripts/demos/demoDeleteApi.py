import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re
from tools.format import readable_json
from tools.auth_token import get_csrf_token
from tools.apis import delete_api_version, delete_api

# Get csrf token
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

'''
    Example of deleting API version.
'''
apiVersionId = '164ecde0-35c9-41cb-9cf8-33bc1007525b.travelportAPI'
deleteApiVersionResp = delete_api_version(csrfToken, apiVersionId)

if deleteApiVersionResp == 200:
    print 'API version deleted successfully.'
else:
    print 'API version deletion failed.'

# '''
#     Example of deleting API and all of its versions.
# '''
# apiId = '76f6f048-5ebd-4868-bf3c-681302f84b53.travelportAPI'
# deleteApiResp = delete_api(csrfToken, apiId)

# if deleteApiResp == 200:
#     print 'API deleted successfully.'
# else:
#     print 'API deletion failed.'
