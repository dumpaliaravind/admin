import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os, re
from tools.format import readable_json
from tools.auth_token import get_csrf_token
from tools.apis import upload_file_to_dropbox, create_api_with_file, get_apis_list, create_api

# Get csrf token
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

swaggerFilePath = 'test_files/demo_api1.json'

create_api(csrfToken, swaggerFilePath)