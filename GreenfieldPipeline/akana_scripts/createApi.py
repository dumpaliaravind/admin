import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re, inspect
from shutil import copyfile
from tools.format import readable_json
from tools.auth_token import get_csrf_token
from tools.apis import upload_file_to_dropbox, create_api_with_file, get_apis_list, create_api, get_api_info, add_doc_to_api


# Check and set host environment variable
pipelineEnv = os.environ.get('ENVIRONMENT')
endpoint, pm_env = None, None

if pipelineEnv == None:
    pm_env = socket.gethostname()[3:5]
else:
    if pipelineEnv not in ['dv', 'pp', 'pn']:
        print 'Error: Pipeline environment varialble incorrect.  Place correct environment variables in pipeline script.  Options: dv, pp, pn.'
        exit()
    else:
        pm_env = pipelineEnv


# Get csrf token
csrfToken = get_csrf_token(os.environ.get('Akanauser'), os.environ.get('Akanapass'))


# Create API from template files
os.chdir('..')
jenkinsProjectName = os.environ.get('JENKINSPROJECTNAME')
jenkinsBuildName = os.environ.get('JENKINSBUILDNAME')
swaggerFilePath = '/var/jenkins_home/workspace/{}/{}/src/main/resources/sample_swagger.json'.format(jenkinsProjectName, jenkinsBuildName)
sampleTextFilePath = '/var/jenkins_home/workspace/{}/{}/apidocs/sample_file.txt'.format(jenkinsProjectName, jenkinsBuildName)

targetName = os.environ.get('APINAME')
targetName = targetName.replace(" ", "") # Remove any whitespaces in name
apiDescription = os.environ.get('APIDESCRIPTION')
create_api(csrfToken, swaggerFilePath, targetName, apiDescription)

# Get version id of target API
apiList = get_apis_list(csrfToken)
apiId = None
apiVerId = None
for api in range(len(apiList)):
    apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
    if apiInfo['Name'] == targetName:
        apiId = apiInfo['APIID']
        apiVerId = apiInfo['LatestVersionID']

if apiId != None and apiVerId != None:
    # Add new versioned toc and sample files
    os.chdir('..')
    dstPath = '/var/jenkins_home/workspace/{}/{}/apidocs/{}'.format(jenkinsProjectName, jenkinsBuildName, apiVerId)
    srcPath = '/var/jenkins_home/workspace/{}/{}/apimgmt/toc.demoAppId.travelportAPI.json'.format(jenkinsProjectName, jenkinsBuildName)
    srcPathSampleFile1 = '/var/jenkins_home/workspace/{}/{}/apimgmt/sample_file_1.txt'.format(jenkinsProjectName, jenkinsBuildName)
    srcPathSampleFile2 = '/var/jenkins_home/workspace/{}/{}/apimgmt/sample_file_2.txt'.format(jenkinsProjectName, jenkinsBuildName)
    dstFile = '{}/toc.{}.json'.format(dstPath, apiVerId)
    dstSampleFile1 = '{}/sample_file_1.txt'.format(dstPath)
    dstSampleFile2 = '{}/sample_file_2.txt'.format(dstPath)

    try:
        if not os.path.exists(dstPath):
            os.makedirs(dstPath)
            copyfile(srcPath, dstFile)
            print 'Default TOC file created for version - ' + apiVerId 
            copyfile(srcPathSampleFile1, dstSampleFile1)
            copyfile(srcPathSampleFile2, dstSampleFile2)
            print 'Sample files created for version - ' + apiVerId 
        else:
            print 'Skipped TOC and sample file creation. Version - ' + apiVerId + ' exists'
    except IOError, e:
        print '{} > {}() > error = {}'.format(sys.argv[0], inspect.stack()[0][3], e)


    # Add toc to API
    addFileResp = add_doc_to_api(csrfToken, dstFile, id=apiId)
    if addFileResp == 200: 
        print 'TOC file added to API successfully.' 
    else:
        print 'TOC file addition to API failed.'

    # Add sample files to API
    addFileResp = add_doc_to_api(csrfToken, dstSampleFile1, id=apiId)
    if addFileResp == 200: 
        print 'Sample file 1 added to API successfully.' 
    else: 
        print 'Sample file 1 addition to API failed.'

    addFileResp = add_doc_to_api(csrfToken, dstSampleFile2, id=apiId)
    if addFileResp == 200: 
        print 'Sample file 2 added to API successfully.' 
    else:
        print 'Sample file 2 addition to API failed.'
else:
    print 'Error: Could not find API ({}) ID/Version ID.'.format(targetName)



