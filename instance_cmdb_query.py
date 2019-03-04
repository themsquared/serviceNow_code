from servicenow import ServiceNow as sn
import requests


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
API_KEY = '---'
APP_KEY = '---'
DATADOG_PREFIX = 'app'

# Go get the JSON permalink to the :
url = "https://"+DATADOG_PREFIX+".datadoghq.com/reports/v2/overview?
api_key="+API_KEY+"&application_key="+APP_KEY+"&metrics=avg%3Aaw
s.ec2.cpuutilization%2Cavg%3Aazure.vm.percentage_cpu%2Cavg%3Agcp
.gce.instance.cpu.utilization%2Cavg%3Asystem.cpu.idle%2Cavg%3Asy
stem.cpu.iowait%2Cavg%3Asystem.load.norm.
15%2Cavg%3Avsphere.cpu.usage&with_apps=true&with_sources=true&wi
th_aliases=true&with_meta=true&with_mute_status=true&with_tags=t
rue"

response = urllib.urlopen(url)
data = json.loads(response.read())
host_json = data['rows']

# For each host in Datadog, look up the corresponding item in SNow and tag it.
for host in host_json:
  hostname = host["name"]
  aliases = host["aliases"]
  sn.updateTags(hostname,sn.attributes(sn.findSysId(url, user, pwd, headers)), API_KEY, APP_KEY)
