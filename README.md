# Automating-Jira-Python
Automation scripts to Jira Cloud using python

* Epic Link Corrector Script

## Configuration
* Make sure Python is installed, any version from v3.x will do
* Required Package → **Requests** can be gotten from [Python](http://python-requests.org)
* Ensure that you have access to the next-gen Project.
* Get an API Token from here [API Token](https://id.atlassian.com/manage/api-tokens) if you haven’t.

## Epic Link Corrector
This Script helps re-link Epic Links to all Standard issue type within a next-gen project that was moved from a Classic Project on Cloud.

### Use Case
Moving from Classic to next-gen project seems like a good idea, but there are lots of things that break up as a result and one of those areas involves Epic Links not showing up on the next-gen Project [JSWCLOUD-18643](https://jira.atlassian.com/browse/JSWCLOUD-18643)
