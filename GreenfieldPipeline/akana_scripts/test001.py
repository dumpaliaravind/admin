import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re, glob
from cStringIO import StringIO
from tools.format import readable_json
from tools.auth_token import get_csrf_token
from tools.apis import upload_file_to_dropbox, create_api_with_file, get_apis_list, create_api, get_policies_for_api
from tools.policies import get_policies_list, policy_attach_format

overwrite = os.environ.get('OVERWRITE')

if overwrite != None:
    if overwrite.lower() == 'true':
        overwrite = True
    else:
        overwrite = False
else:
    overwrite = False

print('overwrite = ', overwrite)