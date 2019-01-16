import requests
import datadog
import json



# The main instance url is https://ven01927.service-now.com/navpage.do where you can find
# the REST API Explorer https://cl.ly/44a3933156d5 <--- Image
# instance_ids = []
# User auth
# Eg. User name="username", Password="password" for this code sample.
user = '---' #'partner.servicenow@datadoghq.com'
pwd = '---'

# This script is limiting the search to one host. This is for a demo.
url = 'https://ven01927.service-now.com/api/now/cmdb/instance/cmdb_ci_linux_server?sysparm_query=*&sysparm_limit=10'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers)

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
    exit()
#data = response.json()
#print(data)

## Pull Server instance/name data from APIs
data = response.json()
for i in data.values():
    for k in i:
        server_url = 'https://ven01927.service-now.com/api/now/cmdb/instance/cmdb_ci_linux_server/{}?sysparm_fields=sys_id%2Cname%2C%2Cu_tag'.format(k['sys_id'])
        # Do the HTTP request
        response = requests.get(server_url, auth=(user, pwd), headers=headers)
        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
            exit()
        dumps = response.json()
        sys_tags = json.dumps(dumps,indent=4, sort_keys=True)
        print(sys_tags)
## Use the Server instance/name data in list to collect tags by server
# url = 'https://ven01927.service-now.com/api/now/cmdb/instance/cmdb_ci_linux_server/{}?sysparm_fields=sys_id%2Ctags'.format(instance_ids)
