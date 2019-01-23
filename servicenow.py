import requests

from json import dumps
from datadog import initialize, api
from jsondiff import diff

class ServiceNow:


    def findSysId(url, user, pwd, headers):
        """(findSysId) GETs the server's instance Id from the cmdb_ci_linux_server table in servicenow."""
        instanceId_url = '{}/api/now/cmdb/instance/cmdb_ci_linux_server?sysparm_query=nameLIKElnux&sysparm_limit=1'.format(url)
        # Do the HTTP request
        response = requests.get(instanceId_url, auth=(user, pwd), headers=headers)
        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
            exit()
        data = response.json()
        sys_id = (data["result"][0]["sys_id"])
        return sys_id, url, user, pwd, headers

    def attributes(data):
        """(attributes) Uses the instance Id collected in the findSysId method and grabs that attributes
        assigned to the server in its servicenow CMDB page.
        """
        sys_id, url, user, pwd, headers = data
        # Set proper headers
        attributes_url = '{}/api/now/cmdb/instance/cmdb_ci_linux_server/{}?sysparm_fields=sys_id%2Cname%2Casset_tag%2Cserial_number'.format(url,sys_id)
        response = requests.get(attributes_url, auth=(user, pwd), headers=headers)
        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
            exit()
        server_dump = response.json()
        #clean_json = dumps(server_dump,indent=4, sort_keys=True)
        attributes = (server_dump["result"]["attributes"])
        return attributes

    def updateTags(host, attrs, api_key, app_key):
        """(updateTags) Uses the hostname parameter to search a host with a mathing name in Datadog.
        Once the host is matched, tags are compared to the attributes using jsondiff. Then finally
        reformated and posted to the Datadog API.
        """
        options = {
            'api_key': api_key,
            'app_key': app_key
            }
        initialize(**options)

        # Get tags by host id.
        hosts = api.Infrastructure.search(q='hosts:{}'.format(host))
        host_tags = (api.Tag.get(hosts['results']['hosts'][0]))
        ddtag_list = host_tags['tags']

        dictlist = []
        # Compare dd tags and servicenow tags
        value = diff(ddtag_list, attrs)
        for n in value.items():
            key, tags = n
            for x, y in sorted(tags.items()):
                dictlist.append("{}:{}".format(x,y))
        if not dictlist:
            print("There are no new tags to submit.")
        else:
            print("Updated tags to {}".format(host))
            api.Tag.update(host, tags=dictlist, source='servicenow')
