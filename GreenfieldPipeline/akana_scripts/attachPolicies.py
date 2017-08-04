import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os
from tools.apis import get_apis_list, get_api_info, get_policies_for_api
from tools.policies import get_policies_list, attach_policy_to_api, policy_attach_format
from tools.auth_token import get_csrf_token
from tools.format import readable_json


# Get policies from groovy env variables
targetPolicies = []
for name in os.environ:
    if name.startswith('OPTIONALPOLICIES'):
        targetPolicies.append(os.environ.get(name))
targetApiName = os.environ.get('APINAME')
overwrite = os.environ.get('OVERWRITE')
print 'These policies are being applied: {}...'.format(targetPolicies)


# Determine if user overwrites current policies
overwrite = os.environ.get('OVERWRITE')
if overwrite != None:
    if overwrite.lower() == 'true':
        overwrite = True
    else:
        overwrite = False
else:
    overwrite = False


csrfToken = get_csrf_token(os.environ.get('Akanauser'), os.environ.get('Akanapass')) 
implementation = os.environ.get('IMPLEMENTATION') 


# Get version id of requested api
apiList = get_apis_list(csrfToken)

apiVersionId = None
for api in range(len(apiList)):
    apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
    if apiInfo['Name'] == targetApiName:
        apiVersionId = apiInfo['LatestVersionID']


# Build list of current policies from api
currentApiPolicies = get_policies_for_api(csrfToken, apiVersionId, implementation)
currentPolicies = []
for currentPolicy in currentApiPolicies['Policy']:
    currentPolicies.append(currentPolicy['Name'])


# Build json policy list to add to api
policiesList = get_policies_list(csrfToken)


# Build available policies list used to check for invalid user policy input
availablePolicies = []
for policy in policiesList:
    formattedPolicy = policy_attach_format(policy)
    availablePolicies.append(formattedPolicy['Name'])

# Build response payload
requestedPolicy = {'Policy': []}
if len(currentApiPolicies['Policy']) > 0 and not overwrite:
    requestedPolicy = currentApiPolicies

if overwrite: print 'Option selected to overwrite current policies...'

badPolicy = False
for targetPolicy in targetPolicies:
    if targetPolicy not in availablePolicies:
        print "\nThere was a problem with this policy = " + str(targetPolicy)
        badPolicy = True

# Attach policies to api if no bad policies were found
if badPolicy:
    print '\nError: Pipeline optional policies variable incorrect.  Place correct policy variables in pipeline script.'
    print '\nAvailable policies:'
    for policy in availablePolicies:
        print(policy)
    print '\n'
    exit()
else:
    for policy in policiesList:
        formattedPolicy = policy_attach_format(policy)
        availablePolicies.append(formattedPolicy["Name"])
        if len(targetPolicies) > 0:
            for targetPolicy in targetPolicies:
                if overwrite and formattedPolicy["Name"] == targetPolicy:
                    requestedPolicy["Policy"].append(formattedPolicy)
                elif formattedPolicy["Name"] == targetPolicy and targetPolicy not in currentPolicies:
                    requestedPolicy["Policy"].append(formattedPolicy)

    # Attach policy to API
    rawData = json.dumps(requestedPolicy)
    policyAttachResp = attach_policy_to_api(csrfToken, rawData, apiVersionId, implementation)

    if policyAttachResp == 200:
        print 'Policy attached to API successfully.'
    else:
        print 'Policy attachment to API failed.'




