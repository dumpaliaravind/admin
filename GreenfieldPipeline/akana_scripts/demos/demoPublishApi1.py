import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re
from tools.format import readable_json
from tools.auth_token import get_csrf_token
from tools.apis import upload_file_to_dropbox, create_api_with_file, get_apis_list

# Get csrf token
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

# Swagger file path location
filePath = 'test_files/tonys_api1_swagger.json'

# Upload swagger file to dropbox
fileUploadedResp, uploadedContent = upload_file_to_dropbox(csrfToken, filePath)

dropboxFileId = uploadedContent['DropboxFileId']
serviceName = uploadedContent['ServiceDescriptorDocument'][0]['ServiceName'][0]

if fileUploadedResp == 200:
    print 'File uploaded successfully.'

    descriptorBody = {
        "DLDescriptor":{
            "ServiceDescriptorReference":{
                "ServiceName":"{}".format(serviceName),
                "FileName":"{}.swagger".format(serviceName),
                "DropboxFileId":dropboxFileId
            }
        }
    }
    descriptorBody = json.dumps(descriptorBody)

    # Create api from uploaded file in dropbox
    apiCreatedResp, apiCreatedContent = create_api_with_file(csrfToken, descriptorBody)

    if apiCreatedResp == 200:
        print 'API created successfully.'
        print 'apiCreatedContent = \n', readable_json(apiCreatedContent)
    else:
        print 'API creation failed.'
else:
    print 'File upload failed.'

