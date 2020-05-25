# Script used for Epic Link Corrector in next-gen Projects
"""
Script   : Epic Link Corrector for Next-gen Projects
Author   : Prince Nyeche
Platform : Atlassian Jira Cloud
Version  : 1.0
**************************************************************************
Required libraries : requests
Download URL       : http://python-requests.org
API Token can be generated from https://id.atlassian.com/manage/api-tokens
**************************************************************************
"""
import json
import requests
from requests.auth import HTTPBasicAuth
import sys


def print_result(data):
    # use the JSON module to load the data
    the_json = json.loads(data.text)
    print("-" * 90)
    read_json(the_json)


# Basic Auth Using python completed within <STDIN>
def jira_basic_auth():
    global email
    global token
    global baseurl
    global pkey
    email = input("Enter your Email Address: \n")
    token = input("Enter your API Token: \n")
    baseurl = input("Enter your Instance Full URL (e.g. nexusfive.atlassian.net) : \n")
    pkey = input("Enter the project key (if multiple projects, separate by comma e.g. NB,NGT,FGT) : \n")
    login(baseurl, email, token, pkey)


# Main function Call here
def main():
    jira_basic_auth()


# simply validate login details
def login(baseurl, email, token, pkey):
    if email == "":
        print("Email Address can't be empty")
        sys.exit(2)
    elif token == "":
        print("Your token can't be empty")
        sys.exit(2)
    elif baseurl == "":
        print("Your Instance Name can't be empty...")
        sys.exit(2)
    elif email and token is not None:
        make_session(email, token, baseurl)
        webURL = ("https://{}/rest/api/3/search/?jql=project%20in%20({})%20AND%20type%20in%20(Epic)"
                  .format(baseurl, pkey))
        data = requests.get(webURL, auth=auth_request, headers=headers)
        if data.status_code == 200:
            print("Login Successful...\n")
            print_result(data)
        else:
            sys.stderr.write("Authentication Failed...")
            sys.exit(1)
    else:
        print("Something went wrong while trying to login...")
        sys.exit(1)


# running get request for authentication and request
def make_session(email, token, baseurl):
    global auth_request
    global headers
    auth_request = HTTPBasicAuth(email, token)
    headers = {"Content-Type": "application/json"}


# reading the epic only issue types
def read_json(the_json):
    print("Searching Issues Keys " + str(the_json["total"]) + " Epic Issues returned...")
    if list(the_json["issues"]) is not None:
        total = the_json["total"]
        maxResults = 50
        startAt = 0
        fullNumber = int(total / 1)
        while total > maxResults or total < maxResults:
            if startAt < fullNumber:
                webEx = ("https://{}/rest/api/3/search/?jql=project%20in%20({})%20AND%20type%20in%20(Epic)"
                         "&startAt={}&maxResults={}".format(baseurl, pkey, startAt, maxResults))
                info = requests.get(webEx, auth=auth_request, headers=headers)
                nu_json = json.loads(info.content)
                for z in list(nu_json["issues"]):
                    print("Reading Epic: " + z["key"])
                    get_epic(z)

            startAt += 50
            if startAt > (fullNumber - 1):
                break


# function to get only Epic Issue type, and find all the associated standard issue type
# from the changelog history
def get_epic(z):
    print("Matching, Issue key {} to URL...".format(z["key"]))
    webURL = ("https://{}/rest/api/3/issue/{}/changelog".format(baseurl, z["key"]))
    data = requests.get(webURL, auth=auth_request, headers=headers)
    pjson = json.loads(data.content)
    if data.status_code != 200:
        print("Error: Unable to access the Changelog History...\n", pjson, sep="-")
    else:
        if z["key"] is not None:
            for i in pjson["values"]:
                fetch = i["items"]
                if fetch is not None:
                    for j in fetch:
                        if j["field"] == "Epic Child":
                            print("Output", j["field"], j["toString"], sep=":")
                            get_current_issue_key((j["field"], j["toString"]), z)
                else:
                    print("Epic Child could not be found...")
        else:
            print("No data from JSON payload...Check again")

        print("*" * 90)
        print("EPIC LINK CORRECTOR COMPLETED, PLEASE CHECK YOUR NEXT-GEN ISSUE @ https://"
              + baseurl + "/browse/" + z["key"])
        print("*" * 90)


# this function gets the current issue key of an issue since it is likely different on the
# changelog history
def get_current_issue_key(j, z):
    if j[1] is None:
        print(f"It seems a \"{j[1]}\" value is detected, we should skip this")
    else:
        webURL = ("https://{}/rest/api/3/issue/{}".format(baseurl, j[1]))
        data = requests.get(webURL, auth=auth_request, headers=headers)
        ijson = json.loads(data.content)
        if data.status_code != 200:
            print("Error: Unable to access the issue's current Issue key...\n", ijson, sep="-")
        else:
            # getting the correct issue key
            if ijson["key"] is not None:
                print("Getting current Issue Key Values of Epic Child  ")
                print("Correct Key : " + ijson["key"])
                print("#" * 90)
                add_child_to_epic(ijson, z)


# this function adds the child issues to the main Epic, using the Edit issue endpoint
def add_child_to_epic(ijson, z):
    print("Dumping Epic Child id " + ijson["id"] + " to Parent Issue... " + z["key"])
    webURL = ("https://{}/rest/api/3/issue/{}".format(baseurl, ijson["id"]))
    payload = (
        {
            "fields": {
                "parent":
                    {
                        "key": z["key"]
                    }

            }
        }
    )
    response = requests.put(webURL, json=payload, auth=auth_request, headers=headers)
    if response.status_code != 204:
        print("Error: Unable to Post the Data Child {} to the Issue {} with Status Code {} \n"
              .format(ijson["key"], z["key"], response.status_code))
        print("*" * 90)
    else:
        print("Epic Child {} Added to Epic {}".format(ijson["key"], z["key"]))
        print("*" * 90)


# Main Program Initialization here
if __name__ == "__main__":
    main()
