# serviceNow_code
A few scripts that sync tags from Servicenow CMDB to Datadog. 
As well as an xml to json conversion script to help those collecting tags from the XML dumps in servicenow.

## Support
Currently only runs on `python3` and requires the dependancy [`jsondiff`](https://pypi.org/project/jsondiff/).

`sudo -H pip3 install jsondiff`

You will need:
A servicenow instance running and a Datadog account where you have the agent running on 
the hosts that you want to sync tags with. Reason for this script is if you want servicenow to be your one source
of truth and Datadog hosts tags to reflect your server attributes in servicenow's CMDB.

## How To RUN
Run the `instance_cmdb_query.py` file directly to start the process. The code is self documented,
most of the data that needs to be entered can be done from this page.

`python3 instance_cmdb_query.py`
