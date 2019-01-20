import yaml
import requests

from xmljson import badgerfish as bf
from json import dumps
from collections import OrderedDict
from datadog import initialize, api
from jsondiff import diff

class ServiceNow:
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    def findSysId(instance, url, user, pwd, headers):
        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)
        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
            exit()
        data = response.json()
        sys_id = (data["result"][0]["sys_id"])
        return sys_id

    def attributes(data , url, user, pwd, headers):
        # Set proper headers
        server_url = 'https://ven01927.service-now.com/api/now/cmdb/instance/cmdb_ci_linux_server/{}?sysparm_fields=sys_id%2Cname%2Casset_tag%2Cserial_number'.format(data)
        response = requests.get(server_url, auth=(user, pwd), headers=headers)
        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
            exit()
        server_dump = response.json()
        #clean_json = dumps(server_dump,indent=4, sort_keys=True)
        attributes = (server_dump["result"]["attributes"])
        return attributes

    def updateTags(host, attrs, api_key, app_key):
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
