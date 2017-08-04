import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re
from tools.format import readable_json
from tools.auth_token import get_csrf_token, get_csrf_token_with_email
from tools.apis import export_api, get_apis_list, import_api

# Get csrf token
# csrfToken = get_csrf_token(os.environ.get('Akanauser'), os.environ.get('Akanapass'))
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

appId = '3ec5855b-e706-43f9-be3d-a4c6b0f9e0ee.travelportAPI'
devPortalTenantEndpoint = 'apiportal'
devBrandingTenantEndpoint = 'apiportalbranded'
zipFileDestPath = 'test_files/api-export.zip'
tenantId = 'travelportAPI'

exportStatus = export_api(csrfToken, devPortalTenantEndpoint, appId, zipFileDestPath)
if exportStatus == 200:
    print 'API exported successfully.'

else:
    print 'API export failed.'

# importStatus = import_api(csrfToken, devPortalTenantEndpoint, tenantId, zipFileDestPath)
# if importStatus == 200:
#     print 'API imported successfully.'
# else:
#     print 'API import failed.'


