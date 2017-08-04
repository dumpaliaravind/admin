import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re
from tools.format import readable_json
from tools.auth_token import get_csrf_token
from tools.apis import upload_file_to_dropbox, create_api_with_file, get_apis_list, create_api, create_new_api_version

# Get csrf token
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

apiGuid = 'aeb532b5-8daf-46db-93e5-85d9266420b5.travelportAPI'
apiName = 'v2'
apiDescription = 'New version 2 of jeffreys_api1_v1_live'
sourceApiVersionId = 'e3d37d7f-c2ff-447c-b7ab-6ba98db3152a.travelportAPI'

createNewApiVersionResp, createNewApiVersionContent = create_new_api_version(csrfToken, apiGuid, apiName, apiDescription, sourceApiVersionId)

if createNewApiVersionResp == 200:
    print 'New API Version created successfully.'
    print 'createNewApiVersionContent = \n', readable_json(createNewApiVersionContent)
else:
    print 'New API Version creation failed.'
