from servicenow import ServiceNow as sn


# EXAMPLE USE OF SERVICENOW TAGS SYNC
# Set the request parameters
# This script is limiting the search to one host. This is for a demo.
instance = "---"
url = 'https://{}.service-now.com'.format(instance)

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Eg. User name="username", Password="password" for this code sample.
user = '---'
pwd = '---'

# Datadog API & APP Keys
api_key = '---'
app_key = '---'

# Hostname that is shared between a servicenow registered server & Datadog
hostname = "lnux100"

sn.updateTags(hostname,sn.attributes(sn.findSysId(url, user, pwd, headers)), api_key, app_key)
