#!/usr/bin/env python

import json, sys, requests, certifi
import smtplib, datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from influxdb import InfluxDBClient

clusters={"ADC_PROD": "api.adc-2a8fde4-gf.travelport.com",
        "ADC_NONPROD":"api.adc-dv-r3yc172-gf.travelport.com",
        "US_EAST":"api.zu2-9vb2qdz-gf.travelport.com",
        "EUROPE_WEST":"api.zew-7d4nwzp-gf.travelport.com",
        "ASIA":"api.zas-udhr3p6-gf.travelport.com"}

proxies = {
  'http': 'http://atlproxy.tvlport.com:8080',
  'https': 'http://atlproxy.tvlport.com:8080',
}

def getData(url,token,params):
        headers = {"Accept": "application/json","Authorization": "bearer " + token}
        # Due to some issues with our Azure servers and TLS, the intermediate CA needs to be added to the default truststore used by python. 
        # The default store can be found by using certifi.where(). The Intermidiate CA is obtained via a browser and then added.
        r = requests.get(url ,params = params, headers=headers, proxies=proxies, verify='/etc/ssl/certs/cacert_custom.pem')#, verify=False)
        data = r.json()
        return data

def sendReport(url, org, emails, level):
        region=""
        for name, vip in clusters.iteritems():
                if vip == url:
                        region = name
        body = ("Your organization memory allocation for applications in " + region + " is above " + level + "% of your Organization's quota. \n"
                "To view your current quota usage go here:\n"
                "https://" + url + "/console/#organizations/" + org['metadata']['guid'] + "/quota\n"
                "To view your usage over time please see our dashboard:\n"
                "http://vhlpnclut001.tvlport.net:31415/dashboard/db/org-dashboard?orgId=1"
                )
        fromaddr = "GreenfieldDeveloperSupport@travelport.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(emails)
        msg['Subject'] = "Organization Quota Report"
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('localhost')
        text = msg.as_string()
        server.sendmail(fromaddr, emails, text)
        server.quit()
#script start
influx = InfluxDBClient('localhost', 8086, None, None, 'stackato_orgs')

for key in clusters:
        print key
        hostname = clusters[key]
        #Get the token first. Insert actual username and password.
        body = "username=<username>&password=<password>&grant_type=password"
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "application/json","Authorization": "Basic Y2Y6"}
        r = requests.post("https://" + hostname + "/uaa/oauth/token", data=body, headers=headers, proxies=proxies, verify='/etc/ssl/certs/cacert_custom.pem')#, verify=False)
        token = r.json()['access_token']
        #adding inline-relations-depth returns more data so less calls needed
        orgs = getData("https://" + hostname + "/v2/organizations?inline-relations-depth=1",token, None)['resources']
        for org in orgs:
                quota = org['entity']['quota_definition']['entity']
                memory_limit = int(quota['memory_limit'])
                routes_limit = int(quota['total_routes'])
                services_limit = int(quota['total_services'])
                spaces = getData("https://" + hostname + org['metadata']['url'] + "/summary?include-relations=app-usage", token, None)['spaces']
                totalAllocated = 0.0
                totalUsed = 0.0
                totalServices = 0
                totalRoutes = 0
                for space in spaces:
                        allocated = float(space['mem_dev_total'])
                        totalAllocated += allocated
                        current = float(space['mem_usage'])
                        totalUsed += current
                        services = int(space['service_count'])
                        totalServices += services
                        routes = len(getData("https://" + hostname +"/v2/spaces/" + space['guid'] + "/routes", token, None)['resources'])
                        totalRoutes += routes
                        measurement = [
                                {
                                "measurement": "quotas_spaces",
                                "tags": {
                                        "org":org['entity']['name'],
                                        "space":space['name'],
                                        "region":key
                                        },
                                "time": datetime.datetime.now(),
                                "fields": {
                                        "memory_usage": current,
                                        "memory_allocated": allocated,
                                        "services": services,
                                        "routes": routes
                                         }
                                }
                        ]
                        influx.write_points(measurement)
                #measurement for each org
                measurement = [
                        {
                                "measurement": "quotas_orgs",
                                "tags": {
                                        "org": org['entity']['name'],
                                        "region": key
                                        },
                                "time": datetime.datetime.now(),
                                "fields": {
                                        "memory_usage": totalUsed,
                                        "memory_allocated": totalAllocated,
                                        "memory_limit":memory_limit,
                                        "services": totalServices,
                                        "services_limit":services_limit,
                                        "routes":totalRoutes,
                                        "routes_limit":routes_limit
                                         }
                        }
                ]
                influx.write_points(measurement)
                notify=False
                if len(sys.argv) > 1:
                        value = totalAllocated/memory_limit
                        print value
                        if len(sys.argv) == 2:
                                if value > float(sys.argv[1])/100.0:
                                        notify=True
                        if len(sys.argv) == 3:
                                range1=float(sys.argv[1])/100.0
                                range2=float(sys.argv[2])/100.0
                                if range1 < value and value < range2:
                                        notify=True
                if notify==True:
                        managers = org['entity']['managers']
                        if len(managers) > 0:
                                query = '{"attributes":["emails"],"guids":['
                                for manager in managers:
                                        guid = manager['entity']['guid']
                                        query += '"' + guid + '",'
                                query = query[:-1]
                                params = {'q': query + "]}"}
                                users = getData("https://" + hostname + "/v2/stackato/users", token, params)['resources']
                                emails = []
                                for user in users:
                                        es = user['emails']
                                        for e in es:
                                                emails.append(e['value'])
                                sendReport(hostname, org, emails, sys.argv[1])
