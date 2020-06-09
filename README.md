# Automating Jira Python
Automation scripts to Jira Cloud using python. below will show case scripts used for performing different functions or solving issues on Jira Cloud.

1. Epic Link Corrector Script

## Configuration
* Make sure [Python](https://www.python.org/downloads/) is installed, any version from v3.x will do
* Required Package → **[Requests](http://python-requests.org)**
* You should have PIP installed with the python download, install request by using `$:pip install requests` on your terminal.
* Ensure that you have access to the next-gen Project.
* Get an API Token from here [API Token](https://id.atlassian.com/manage/api-tokens) if you haven’t.

## Epic Link Corrector
This Script helps re-link Epic Links to all Standard issue type within a next-gen project that was moved from a Classic Project on Cloud.

### Use Case
Moving from Classic to next-gen project seems like a good idea, but there are lots of things that break up as a result and one of those areas involves Epic Links not showing up on the next-gen Project [JSWCLOUD-18643](https://jira.atlassian.com/browse/JSWCLOUD-18643)

### How to Use
1. Go to your **terminal** (macOS/linux) or **command prompt** (windows) and `cd` into the directory where the script is stored.
2. Start by using `$:python epiclc.py` or whatever you've named the script as
3. Follow the prompt to authenticate your user and search the next-gen projects that needs corrections.
