from xmljson import badgerfish as bf
from json import dumps
from collections import OrderedDict
from xml.etree.ElementTree import fromstring

import requests

# Open xml file and use contents

##Use stdout of open/read func for conversion function
## Write the new converted json to file

# Collect entrie host list from Datadog and ServiceNow (Compare)
# For hosts in serviceNow that exist in Datadog search tags
# Compare existing tags in both APIs, if serviceNow tags don't exist in Datadog update hosts from list
# Parse new json file and update Datadog host tags **Dep**: datadog

#Instance
instance = '---'

# Set the request parameters
url = 'https://'+instance+'.service-now.com/api/now/table/problem?sysparm_limit=1'

# Eg. User name="username", Password="password" for this code sample.
user = '---' #'partner.servicenow@datadoghq.com'
pwd = '---'

# Set proper headers
headers = {"Content-Type":"application/xml","Accept":"application/xml"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers)

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
    exit()

# Decode the XML response into a dictionary and use the data
# print(response.content)
new_json = dumps(bf.data(fromstring(response.content)),indent=4, sort_keys=True)
print(new_json)
