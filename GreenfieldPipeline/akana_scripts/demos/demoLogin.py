import urllib, urllib2, base64, socket, smtplib, ssl, sys, cookielib, json, os
from tools.auth_token import get_csrf_token

# Get csrf token
csrfToken = get_csrf_token('Akana_svc', 'Pass2017')
print 'csrfToken = ', csrfToken

