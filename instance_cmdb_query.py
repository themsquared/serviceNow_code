from servicenow import ServiceNow as sn
# Set the request parameters
# This script is limiting the search to one host. This is for a demo.
url = 'https://ven01927.service-now.com/api/now/cmdb/instance/cmdb_ci_linux_server?sysparm_query=nameLIKElnux&sysparm_limit=1'
#url = 'https://'+instance+'.service-now.com/api/now/table/problem?sysparm_limit=1'
#server_url = 'https://ven01927.service-now.com/api/now/cmdb/instance/cmdb_ci_linux_server/{}?sysparm_fields=sys_id%2Cname%2Casset_tag'.format(k['sys_id'])
# Eg. User name="username", Password="password" for this code sample.
user = '---' #'partner.servicenow@datadoghq.com'
pwd = '---'
api_key = '---'
app_key = '---'

sn.updateTags("lnux100",sn.attributes(sn.findSysId(url, user, pwd),url, user, pwd), api_key, app_key)
