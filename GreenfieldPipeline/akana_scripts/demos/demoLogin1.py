import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os
from tools.auth_token import get_csrf_token
print os.environ.get('APINAME')
print os.environ.get('myuser')
print os.environ.get('mpass')
# Get csrf token
#csrfToken = get_csrf_token(os.environ.get['myuser' ,'mypass'])
csrfToken = get_csrf_token(os.environ.get('myuser'), os.environ.get('mypass'))
#csrfToken = get_csrf_token('Akana_svc', 'Pass2017')

print 'csrfToken = ', csrfToken

