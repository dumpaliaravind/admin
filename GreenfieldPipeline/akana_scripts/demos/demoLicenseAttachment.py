import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os
from tools.format import readable_json
from tools.apis import get_apis_list, get_api_info
from tools.auth_token import get_csrf_token
from tools.licenses import get_licenses_for_api, add_licenses, get_resources_for_api, get_scopes_for_api, get_private_viewer_scopes_for_api, add_scope, add_scope_mapping_to_api

targetApiName = 'jeffreys_api1_v1_live'
businessId = 'tenantbusiness.travelportAPI'

# Get csrf token
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

# # Add scope
# scopeData = {
#   "ResourceID": "",
#   "Name": "Silver access",
#   "ShortDescription": "Silver access",
#   "LongDescription": "Silver access",
#   "Visibility": "Public",
#   "SandboxAnonymousAccessAllowed": "false",
#   "ProductionAnonymousAccessAllowed": "false",
#   "ResourcePath": "",
#   "OAuthGrantDefaultResource": "true",
#   "OAuthGrantUserAuthorizationRequired": "true",
#   "ParentResourceID": "",
#   "BusinessID": businessId
# }
# scopeData = json.dumps(scopeData)

# addScopeResp, addScopeContent = add_scope(csrfToken, businessId, scopeData)
# print 'addScopeResp = ', addScopeResp
# print 'addScopeContent = ', readable_json(addScopeContent)


# # Add license
# licenseData = {
#   "Environment":[
#     "Sandbox",
#     "Production"
#   ],
#   "Visibility":"Limited",
#   "SandboxAccessAutoApproved":"true",
#   "ProductionAccessAutoApproved":"false",
#   "Active":'true',
#   "AgreementDetails":{
#     "AgreementDocument":[
      
#     ]
#   },
#   "Name":"Custom License 1",
#   "Description":"Terms - 100 requests per second / Approval Required",
#   "LicenseParts":{
#     "LicensePart":[
#       {
#         "ResourceID":[
#           "93b0b138-6515-4c08-99a0-27b6db19f1b0.travelportAPI"
#         ],
#         "PolicyKey":[

#         ]
#       }
#     ]
#   },
#   "BusinessID":businessId
# }
# licenseData = json.dumps(licenseData)

# addLicenseResp, addLicenseContent = add_licenses(csrfToken, licenseData)
# print 'addLicenseResp = ', addLicenseResp
# print 'addLicenseContent = ', readable_json(addLicenseContent)


# Add scope mapping to API
apiVersionId = '23aeb8fb-d857-44b4-a2bc-36db0e29f98b.travelportAPI'
scopeMappingData = {
  "OperationResource":[
    {
      "OperationName":"Silver access",
      "ResourceID":[
        "93b0b138-6515-4c08-99a0-27b6db19f1b0.travelportAPI"
      ]
    }
  ]
}
scopeMappingData = json.dumps(scopeMappingData)

addScopeMappingResp, addScopeMappingContent = add_scope_mapping_to_api(csrfToken, apiVersionId, scopeMappingData)

if addScopeMappingResp == 200:
    print 'Scope added to API successfully.'
    print 'addScopeMappingContent = ', readable_json(addScopeMappingContent)
else:
    print 'Scope addition to API failed.'






    