# -*- coding: utf-8 -*-
import urllib, urllib2, json, ssl, socket, httplib, mimetypes, sys, inspect, os
import itertools, mimetools, mimetypes
from cStringIO import StringIO
from tools.multipart_form import MultiPartForm
from tools.format import readable_json
from tools.policies import get_policies_list, policy_attach_format, attach_policy_to_api

# Check and set host environment variable
pipelineEnv = os.environ.get('ENVIRONMENT')
endpoint, pm_env = None, None

if pipelineEnv == None:
    pm_env = socket.gethostname()[3:5]
else:
    if pipelineEnv not in ['dv', 'pp', 'pn']:
        print('Pipeline environment varialble incorrect.  Place correct environment variables in pipeline script.  Options: dv, pp, pn.')
        exit()
    else:
        pm_env = pipelineEnv

if(pm_env == 'dv'):
    endpoint, tenantHost = 'apiportal.dv.tvlport.com', 'dv.tvlport.com'
elif(pm_env == 'pp'):
    endpoint, tenantHost = 'apiportal.pp.tvlport.com', 'pp.tvlport.com'
elif(pm_env == 'pn'):
    endpoint, tenantHost = 'apiportal.travelport.com', 'travelport.com'
else:
    endpoint, tenantHost, pm_env = 'apiportal.pp.tvlport.com', 'pp.tvlport.com', 'pp'   # Default to PP when testing locally

# Set ciphers and ssl settings
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
ctx.set_ciphers('HIGH:!DH:!aNULL')

# Set proxy settings
proxy = urllib2.ProxyHandler({'https':'atlproxy.tvlport.com:443', 'http':'atlproxy.tvlport.com:8080'})
opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx), proxy)
urllib2.install_opener(opener)

def get_apis_list(token):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
    OUTPUT  1. (array) - List of APIs.
    '''
    apisURL = 'https://{}/api/apis'.format(endpoint)
    apisHeaders = {'Accept':'application/json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=apisURL, headers=apisHeaders)
        getApisResp = json.loads(urllib2.urlopen(request).read())

        apiList = []
        for api in range(len(getApisResp['channel']['item'])):
            apiList.append(getApisResp['channel']['item'][api])
        return apiList
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def get_policies_for_api(token, apiGuid, implementation):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiGuid (string) - API version id.
            3. implementation (string) - Implementation environment, either 'live' or 'sandbox'.
    OUTPUT  1. (json) - List of policies for API.
    '''
    apiPoliciesUrl = 'https://{}/api/apis/versions/{}/implementations/{}/policies'.format(endpoint, apiGuid, implementation)
    apiPoliciesHeaders = {'Accept':'application/json, text/javascript, */*; q=0.01', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=apiPoliciesUrl, headers=apiPoliciesHeaders)
        return json.loads(urllib2.urlopen(request).read())
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def get_api_info(token, apiGuid):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiGuid (string) - API id.
    OUTPUT  1. (json) - Information about API.
    '''
    apiInfoUrl = 'https://{}/api/apis/{}'.format(endpoint, apiGuid)
    apiInfoHeaders = {'Accept':'application/json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=apiInfoUrl, headers=apiInfoHeaders)
        return json.loads(urllib2.urlopen(request).read())
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def get_api_versions(token, apiGuid):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiGuid (string) - API id.
    OUTPUT  1. (json) - Information about API versions.
    '''
    apiVersionsUrl = 'https://{}/api/apis/{}/versions'.format(endpoint, apiGuid)
    apiVersionsHeaders = {'Accept':'application/json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=apiVersionsUrl, headers=apiVersionsHeaders)
        return json.loads(urllib2.urlopen(request).read())
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def get_swagger_doc_for_api(token, apiVersionId):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiVersionId (string) - Version id for API.
    OUTPUT  1. (json) - Swagger document in json.
    '''
    swaggerDocUrl = 'https://{}/api/apis/versions/{}/definition/swagger'.format(endpoint, apiVersionId)
    swaggerDocHeaders = {'Accept':'application/json, text/javascript, */*; q=0.01', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=swaggerDocUrl, headers=swaggerDocHeaders)
        return json.loads(urllib2.urlopen(request).read())
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def upload_file_to_dropbox(token, filePath):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. filePath (string) - File path of file to upload.
    OUTPUT  1. (int) – HTTP response code from request
            2. (json) – Uploaded content response with information about the service that will be used to create the API.
    '''
    dropboxUploadUrl = 'https://{}/api/dropbox/readfiledetails'.format(endpoint)
    
    fileName = filePath.split("/", 1)[1]
    form = MultiPartForm()
    form.add_file('swagger', fileName, fileHandle=StringIO(open(filePath, 'rb').read()))
    body = str(form)

    # Build request
    request = urllib2.Request(dropboxUploadUrl)
    request.add_header('Accept', 'application/json, application/vnd.soa.v81+json')
    request.add_header('X-Csrf-Token_travelportAPI', token)
    request.add_header('Content-Type', form.get_content_type())
    request.add_header('Content-Length', len(body))
    request.add_data(body)

    try:
        postDropboxUpload = urllib2.urlopen(request)
        fileUploadedResp = postDropboxUpload.getcode()
        uploadedContent = postDropboxUpload.read()
        return fileUploadedResp, json.loads(uploadedContent)
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def create_api_with_file(token, descriptorBody):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. descriptorBody (json) – API description document.
    OUTPUT  1. (int) – HTTP response code from request.
    '''
    createApiWithFileUrl = 'https://{}/api/apis'.format(endpoint)
    createApiWithFileHeaders = {'Accept':'application/vnd.soa.v81+json', 'Content-Type':'application/vnd.soa.v81+json', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=createApiWithFileUrl, headers=createApiWithFileHeaders, data=descriptorBody)
        request.get_method = lambda: 'POST'
        postCreateApi = urllib2.urlopen(request)
        postCreateApiResp = postCreateApi.getcode()
        postCreateApiContent = postCreateApi.read()
        return postCreateApiResp, json.loads(postCreateApiContent)
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def add_doc_to_api(token, filePath, id):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. filePath (string) - File path of document to upload.
            3. id (string) - App id or version id.
    OUTPUT  1. (int) – HTTP response code from request.
    '''
    addFileToApiUrl = 'https://{}/content/api/{}/documents'.format(endpoint, id)

    fileName = filePath.split("/", 1)[1]
    form = MultiPartForm()
    form.add_file('file', fileName, fileHandle=StringIO(open(filePath, 'rb').read()))
    body = str(form)

    # Build request
    request = urllib2.Request(addFileToApiUrl)
    request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request.add_header('X-Csrf-Token_travelportAPI', token)
    request.add_header('Content-Type', form.get_content_type())
    request.add_header('Content-Length', len(body))
    request.add_data(body)

    try:
        return urllib2.urlopen(request).getcode()
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def create_sandbox_impl(token, apiVerId):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
    OUTPUT  1. (int) – HTTP response code from request.
            2. (json) – Iinformation about the implementation that was added.
    '''
    createSandboxImplUrl = 'https://{}/api/apis/versions/{}/implementations'.format(endpoint, apiVerId)
    createSandboxImplHeaders = {'Accept':'application/vnd.soa.v81+json, text/javascript, */*; q=0.01', 'Content-Type':'application/vnd.soa.v81+json', 'X-Csrf-Token_travelportAPI':token}

    sandboxImplBody = {
        "ImplementationCode":"Sandbox",
        "Description":"Sandbox implementation.",
        "CreateMechanism":"PROXY",
        "ProxyImplementationRequest":{
            "TargetEndpointURL":[

            ]
        },
        "APIVersionID":apiVerId
    }
    sandboxImplBody = json.dumps(sandboxImplBody)

    try:
        request = urllib2.Request(url=createSandboxImplUrl, headers=createSandboxImplHeaders, data=sandboxImplBody)
        request.get_method = lambda: 'POST'
        postCreateSandboxImpl = urllib2.urlopen(request)
        postCreateSandboxImplResp = postCreateSandboxImpl.getcode()
        postCreateSandboxImplContent = postCreateSandboxImpl.read()
        return postCreateSandboxImplResp, json.loads(postCreateSandboxImplContent)
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def create_api(token, swaggerFilePath, apiName, apiDescription):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. swaggerFilePath (string) - File path of swagger document to upload.
    OUTPUT  None
    '''
    # Update swagger with new name and description
    swaggerJsonFile = json.load(open(swaggerFilePath))
    swaggerJsonFile['info']['title'] = apiName
    swaggerJsonFile['info']['description'] = apiDescription
    updatedSwaggerFile = open(swaggerFilePath, 'w+')
    updatedSwaggerFile.write(json.dumps(swaggerJsonFile))
    updatedSwaggerFile.close()

    fileUploadedResp, uploadedContent = upload_file_to_dropbox(token, swaggerFilePath)

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
        apiCreatedResp, apiCreatedContent = create_api_with_file(token, descriptorBody)

        if apiCreatedResp == 200:
            print 'API created successfully.'
            print 'apiCreatedContent = \n', readable_json(apiCreatedContent)

            # Add default policies
            defaultPolicies = ['BasicAuditing', 'Travelport AppID', 'Travelport LDAP Authentication', 'Travelport Tracking ID']
            apiName = apiCreatedContent['Name']
            apiVersionId = apiCreatedContent['LatestVersionID']

            # Display list of all policies
            policiesList = get_policies_list(token)

            # Build json policy list to add to api
            requestedPolicy = {"Policy": []}

            for policy in policiesList:
                formattedPolicy = policy_attach_format(policy)
                if len(defaultPolicies) > 0:
                    for targetPolicy in defaultPolicies:
                        if formattedPolicy["Name"] == targetPolicy:
                            requestedPolicy["Policy"].append(formattedPolicy)

            # Attach policy to API 
            rawData = json.dumps(requestedPolicy)

            policyAttachResp = attach_policy_to_api(token, rawData, apiVersionId, 'live')

            if policyAttachResp == 200:
                print 'Policy attached to API successfully.'
            else:
                print 'Policy attachment to API failed.'
            
            # Create sandbox implementation
            postCreateSandboxImplResp, postCreateSandboxImplContent = create_sandbox_impl(token, apiVersionId)
            if postCreateSandboxImplResp == 200:
                print 'Sandbox implementation created successfully.'
            else:
                print 'Sandbox implementation creation failed.'
        else:
            print 'API creation failed.'
        print 'File upload successfull.'
    else:
        print 'File upload failed.'

def create_new_api_version(token, apiGuid, apiName, apiDescription, sourceApiVersionId):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiGuid (string) - API version id.
            3. apiName (string) - Name of new API.
            4. apiDescription (string) - Description of new API.
            5. sourceApiVersionId (string) - API version id of source used to make new API version.
    OUTPUT  1. (int) – HTTP response code from request.
            2. (json) – Information about the new API version.
    '''
    createNewApiVersionUrl = 'https://{}/api/apis/{}/versions'.format(endpoint, apiGuid)
    createNewApiVersionHeaders = {'Accept':'application/vnd.soa.v81+json', 'Content-Type':'application/vnd.soa.v81+json', 'X-Csrf-Token_travelportAPI':token}

    apiRequestBody = {
        "APIVersionInfo":{
            "Name":apiName,
            "Description":apiDescription
        },
        "CloneAPIVersionRequest":{
            "SourceAPIVersionID":sourceApiVersionId,
            "CloneDesign":"true",
            "CloneImplementations":"true"
        }
    }
    apiRequestBody = json.dumps(apiRequestBody)

    try:
        request = urllib2.Request(url=createNewApiVersionUrl, headers=createNewApiVersionHeaders, data=apiRequestBody)
        request.get_method = lambda: 'POST'
        postCreateNewApiVersion = urllib2.urlopen(request)
        postCreateNewApiVersionResp = postCreateNewApiVersion.getcode()
        postCreateNewApiVersionContent = postCreateNewApiVersion.read()
        return postCreateNewApiVersionResp, json.loads(postCreateNewApiVersionContent)
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def delete_api_version(token, apiGuid):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiGuid (string) - API version id.
    OUTPUT  1. (int) – HTTP response code from request.
    '''
    deleteApiVersionUrl = 'https://{}/api/apis/versions/{}'.format(endpoint, apiGuid)
    deleteApiVersionHeaders = {'Accept':'text/plain', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=deleteApiVersionUrl, headers=deleteApiVersionHeaders)
        request.get_method = lambda: 'DELETE'
        deleteApiVersion = urllib2.urlopen(request)
        return deleteApiVersion.getcode()
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def delete_api(token, apiGuid):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. apiGuid (string) - API id.
    OUTPUT  1. (int) – HTTP response code from request.
    '''
    deleteApiUrl = 'https://{}/api/apis/{}'.format(endpoint, apiGuid)
    deleteApiHeaders = {'Accept':'text/plain', 'X-Csrf-Token_travelportAPI':token}

    try:
        request = urllib2.Request(url=deleteApiUrl, headers=deleteApiHeaders)
        request.get_method = lambda: 'DELETE'
        deleteApi = urllib2.urlopen(request)
        return deleteApi.getcode()
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def export_api(token, tenantEndpoint, apiGuid, zipFileDestPath):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. tenantEndpoint (string) - Name of tenant used to connect to its endpoint.
            3. apiGuid (string) - API id.
            4. zipFileDestPath (string) - File path to source zip file to upload.
    OUTPUT  1. (int) – HTTP response code from request.
    '''
    exportApiUrl = 'https://{}.{}/api/apis/{}/package?exportVersion=all&migration.operationalpolicy.export=true&migration.qospolicy.export=true&migration.pki.export=true&migration.export.include.api.admins=true&migration.export.include.api.connections=true&migration.export.include.scopes=true&wrapInHTML=true&document.domain=apiportal.{}.tvlport.com&download=true'.format(tenantEndpoint, tenantHost, apiGuid, pm_env)

    print 'exportApiUrl = ', exportApiUrl

    request = urllib2.Request(exportApiUrl)
    request.add_header('Accept', 'application/json, application/octet-stream')
    request.add_header('X-Csrf-Token_travelportAPI', token)

    try:
        file_name = zipFileDestPath
        exportApi = urllib2.urlopen(request)
        zipFile = open(file_name, 'wb')
        meta = exportApi.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = exportApi.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            zipFile.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status

        zipFile.close()
        return exportApi.getcode()
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def import_api(token, tenantEndpoint, tenantId, zipFileDestPath):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. tenantEndpoint (string) - Name of tenant used to connect to its endpoint.
            3. tenantId (string) - Unique ID for a specific tenant.
            4. zipFileDestPath (string) - File path to source zip file to upload.
    OUTPUT  1. (int) – HTTP response code from request.
    '''
    importApiUrl = 'https://{}.{}/api/tenants/{}/packages'.format(tenantEndpoint, tenantHost, tenantId)
    
    fileName = zipFileDestPath.split("/", 1)[1]
    form = MultiPartForm()
    form.add_file('Package', fileName, fileHandle=StringIO(open(zipFileDestPath, 'rb').read()))
    body = str(form)

    # Build request
    request = urllib2.Request(importApiUrl)
    request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request.add_header('X-Csrf-Token_travelportAPI', token)
    request.add_header('Content-Type', form.get_content_type())
    request.add_header('Content-Length', len(body))
    request.add_data(body)

    try:
        return urllib2.urlopen(request).getcode()
    except urllib2.HTTPError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)
        return False

def promote_api(token, sourceTenantEndpoint, targetTenantEndpoint, sourceApiId, targetTenantId, zipFilePath):
    '''
    INPUT   1. token (string) - Cross site request forgery token used to make rest calls to Akana API.
            2. sourceTenantEndpoint (string) - Name of source tenant used to connect to its endpoint.
            3. targetTenantEndpoint (string) - Name of target tenant used to connect to its endpoint.
            4. sourceApiId (string) - API id.
            5. targetTenantId (string) - Unique ID for a specific tenant.
            6. zipFilePath (string) - File path to zip file.
    OUTPUT  1. None
    '''
    exportStatus = export_api(token, sourceTenantEndpoint, sourceApiId, zipFilePath)
    if exportStatus == 200:
        print 'API exported successfully.'
        importStatus = import_api(token, targetTenantEndpoint, targetTenantId, zipFilePath)
        if importStatus == 200:
            print 'API imported successfully.'
        else:
            print 'API import failed.'
    else:
        print 'API export failed.'

