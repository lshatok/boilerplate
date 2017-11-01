#!/usr/bin/env python3
import boto3
import os

#### https://webtelemetry().atlassian.net/wiki/topics/automation/AWS+Console+Security
#### This script should be run for each AWS account.
#### It spits out a csv file that reports user account
#### data for compliance to various security restrictions
#### such as MFA, age of AWS key, AWS groups, etc
#### You don't have to run the script per region,
#### just per AWS account
#### To run: set your aws env key/secret/region and run it

REGION = os.environ.get('AWS_REGION')
client = boto3.client('iam')

# populate all the users
users = client.list_users()

# create your output container
userout = {}

# iterate through the 'Users' key and load up the userout dictionary with password last used
for i in users['Users']:
    userout[i['UserId']] = {}
    userout[i['UserId']]['name'] = i['UserName']
    userout[i['UserId']]['usercreated'] = str(i['CreateDate'])
    if 'PasswordLastUsed' in i.keys():
        userout[i['UserId']]['lastlogin'] = str(i['PasswordLastUsed'])
    else:
        userout[i['UserId']]['lastlogin'] = "none"

# Get groups
for i in userout:
    userout[i]['groups'] = []
    group = client.list_groups_for_user(UserName=userout[i]['name'])
    if not group['Groups']:
        userout[i]['groups'].append('none')
    else:
        for l in group['Groups']:
            userout[i]['groups'].append(l['GroupName'])

# Get mfa serial
for i in userout:
    mfa = client.list_mfa_devices(UserName=userout[i]['name'])
    if not mfa['MFADevices']:
        userout[i]['mfa'] = "none"
    else:
        for l in mfa['MFADevices']:
            userout[i]['mfa'] = l['SerialNumber']

# Get access key ID and status
for i in userout:
    userout[i]['keylist'] = []
    dme = {}
    key = client.list_access_keys(UserName=userout[i]['name'])
    for l in key['AccessKeyMetadata']:
        dme['keystatus'] = l['Status']
        dme['keyid'] = l['AccessKeyId']
        dme['keycreated'] = str(l['CreateDate'])
        userout[i]['keylist'].append(dme.copy())

# Get when the key was last used
if 'gov' not in REGION:
    for i in userout:
        for l in userout[i]['keylist']:
            keyuse = client.get_access_key_last_used(AccessKeyId=l['keyid'])
            if 'LastUsedDate' in keyuse['AccessKeyLastUsed'].keys():
                l['keylast'] = str(keyuse['AccessKeyLastUsed']['LastUsedDate'])
            else:
                l['keylast'] = "none"

# print out csv
print(
    "AccountId, AccountName, Last AWS Login, Account Creation, MFA Token, Groups, API Key1 KeyID, API Key1 Status, API Key1 Creation, API Last Key1 Login, API Key2 KeyID, API Key2 Status, API Key2 Creation, API Last Key2 Login,")

for i in userout:
    print(userout[i]['name'] + ', ' + i + ', ' + userout[i]['lastlogin'] + ', ' + userout[i]['usercreated'] + ', ' +
          userout[i]['mfa'] + ', ' + ' '.join([str(elem) for elem in sorted(userout[i]['groups'])]) + ", ", end="")
    if not userout[i]['keylist']:
        print("no api key")
    else:
        for l in userout[i]['keylist']:
            if 'gov' in REGION:
                # print(l['keyid'] + ', ' + l['keystatus'] + ', not available in gov' + ', ', end="")
                print(
                    l['keyid'] + ', ' + l['keystatus'] + ', ' + l['keycreated'] + ', not available in gov' + ', ',
                    end="")
                else:
                print(l['keyid'] + ', ' + l['keystatus'] + ', ' + l['keycreated'] + ', ' + l['keylast'] + ', ', end="")
                # need to add a newline now that everything is printed out.
                print("")

                # Admins might use this script to check several accounts, one after the other, and >> them into the same csv file, so I'm creating an end statement to separate the lists.
        print("--- End User List for this AWS Account ---")


        #### you don't get a response from get-login-profile if the console password has been disabled
        # 6302-tfewkes:~ tfewkes$ aws iam get-login-profile --user-name khanh.luc 

        # A client error (NoSuchEntity) occurred when calling the GetLoginProfile operation: Cannot find Login Profile for User khanh.luc
        # 6302-tfewkes:~ tfewkes$ aws iam get-login-profile --user-name khanh.luc 
        # {
        # "LoginProfile": {
        # "UserName": "khanh.luc", 
        # "CreateDate": "2017-01-27T20:20:06Z", 
        # "PasswordResetRequired": false
        # }
        # }



        # here's what each key/line in userout looks like:

        # "AIDAIBZTQQZBN5OXEXC4S": {"name": "taydula", "groups": ["DevOps", "Administrators"], "keylist": [{"keystatus": "Active", "keyid": "AKIAIJEWFJAWOULCYCLA", "keylast": "none"}, {"keystatus": "Active", "keyid": "AKIAJBJQZECAZTXK2OYA", "keylast": "2016-11-19 06:29:00+00:00"}], "lastlogin": "2016-12-02 18:55:41+00:00", "mfa": "arn:aws:iam::049795576831:mfa/taydula"},

        # "AIDAI4IUFJSOMFXZAAKSU": {"name": "devops-readonly", "groups": ["nogroup"], "keylist": [{"keystatus": "Active", "keyid": "AKIAIJK7LYS3AZJZRB2A", "keylast": "none"}], "lastlogin": "none", "mfa": "none"}, 

        # "AIDAI6XSHSFXGRR36UYFS": {"name": "austin", "groups": ["DevOps", "EC2manage", "Route53manage", "Administrators"], "keylist": [], "lastlogin": "2016-12-06 20:16:55+00:00", "mfa": "none"}, 

        # "AIDAJ6BHUT4MQGDVRFJ7S": {"name": "ag_server_snapshots", "groups": ["nogroup"], "keylist": [{"keystatus": "Active", "keyid": "AKIAIANT3RWJJE7KKH2Q", "keylast": "2017-01-23 09:58:00+00:00"}], "lastlogin": "none", "mfa": "none"}, 

        # "AIDAJ6JGYB72P6FMHQSBM": {"name": "chris.michael", "groups": ["DevOps", "Administrators"], "keylist": [{"keystatus": "Active", "keyid": "AKIAIMD5DCT6BJSQGEFA", "keylast": "2016-12-21 20:24:00+00:00"}], "lastlogin": "2016-12-20 18:25:04+00:00", "mfa": "arn:aws:iam::049795576831:mfa/chris.michael"},
