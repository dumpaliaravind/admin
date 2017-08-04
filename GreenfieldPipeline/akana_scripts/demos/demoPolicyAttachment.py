import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os
from tools.apis import get_apis_list, get_api_info
from tools.policies import get_policies_list, attach_policy_to_api, policy_attach_format
from tools.auth_token import get_csrf_token
from tools.format import readable_json

targetPolicies = ['DetailedAuditing', 'BasicAuditing', 'Travelport Tracking ID']
targetApiName = 'jeffreys_api1_v1_live'

# Get csrf token
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

# Display list of all policies
policiesList = get_policies_list(csrfToken)

# Build json policy list to add to api
requestedPolicy = {"Policy": []}

for policy in policiesList:
	formattedPolicy = policy_attach_format(policy)
	if len(targetPolicies) > 0:
		for targetPolicy in targetPolicies:
			if formattedPolicy["Name"] == targetPolicy:
				requestedPolicy["Policy"].append(formattedPolicy)

# Get version id of requested api
apiList = get_apis_list(csrfToken)

apiVersionId = None
for api in range(len(apiList)):
	apiInfo = get_api_info(csrfToken, apiList[api]['guid']['value'])
	if apiInfo['Name'] == targetApiName:
		apiVersionId = apiInfo['LatestVersionID']

# Attach policy to API 
rawData = json.dumps(requestedPolicy)

policyAttachResp = attach_policy_to_api(csrfToken, rawData, apiVersionId, 'Live')

if policyAttachResp == 200:
    print 'Policy attached to API successfully.'
else:
    print 'Policy attachment to API failed.'







