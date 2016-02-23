## Splunk_Cymon.io


#### Description

A python script that can be used by a Splunk custom command to query the Cymon.io API. 
If you have any comments or suggestions please raise an issue and I'll get back to you.

#### Requirements

1. Splunk 6.0+ 
2. Internet connection

#### Installation

1. Add the following to your Splunk apps commands.conf
```python
[cyLookup]
filename = cymonsplunk.py
```
2. Add cymonsplunk.py to `$SPLUNK_HOME/etc/apps/<app_name>/bin/`

#### Usage

From Splunk search run `| cymon __EXECUTE__ 8.8.8.8 | spath input=cy`

#### ToDo

- [ ] Add support for API keys
- [ ] Add support for full cymon.io python library (https://github.com/eSentire/cymon-python)
- [ ] Add option for scripted input, e.g inputlookup against proxy or firewall logs.

##### Credits
Used a one or two line snippet of another script but can't remember where I found it from. 
