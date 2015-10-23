import boto3
import os
import sys
import uuid
import gzip
import json
from pprint import pprint

ses_client = boto3.client('ses')
s3_client = boto3.client('s3')

us_west2_ami = ['ami-2e84611d', 'ami-06846135', 'ami-ed9b8bdd', 'ami-d52227e5', 'ami-25190415']
us_east1_ami = ['ami-895617ec', 'ami-0956176c', 'ami-47a0272c', 'ami-edcba488']



def lambda_handler (event, context):
    #pprint(event['Records'])
    print('\n')
    #print json.dumps(event, indent=1)
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}'.format(key)
        print "bucket/key/path", bucket, key, download_path
        download_json_file(bucket, key, download_path)

def download_json_file(bucket, key, download_path):
    s3_client.download_file(bucket, key, download_path)
    with open(download_path, 'rb') as f:
    #with gzip.open(download_path, 'rb') as f:
        data = json.load(f)

        for details in data['Records']:
            if details['eventSource'] == 'ec2.amazonaws.com':
                 if details['eventName'] == 'RunInstances':
                    pprint(details)
                    check_ec2(details)
            if details['eventSource'] == 'iam.amazonaws.com':
                 if details['eventName'] == 'CreateRole':
                    pprint(details)
                    check_iam_role(details)
            if details['eventSource'] == 'iam.amazonaws.com':
                 if details['eventName'] == 'CreateUser':
                    pprint(details)
                    check_iam_user(details)


def check_ec2(i):
    # pprint(i)
    event_details = {}
    event_details['imageiD'] = str(i['responseElements']['instancesSet']['items'][0]['imageId'])
    event_details['instanceId'] = str(i['responseElements']['instancesSet']['items'][0]['instanceId'])
    event_details['instanceType'] = str(i['responseElements']['instancesSet']['items'][0]['instanceType'])
    event_details['keyName'] = str(i['responseElements']['instancesSet']['items'][0]['keyName'])
    event_details['availabilityZone'] = str(i['responseElements']['instancesSet']['items'][0]['networkInterfaceSet']['items'][0]['availabilityZone'])
    event_details['vpcId'] = str(i['responseElements']['instancesSet']['items'][0]['networkInterfaceSet']['items'][0]['vpcId'])
    pprint(event_details)
    #pprint(i['responseElements']['instancesSet']['items'][0]['networkInterfaceSet']['items'][0])

    if not (event_details['imageiD'] in us_west2_ami or event_details['imageiD'] in us_east1_ami):
        print("Not a Gold Image")
        info = """\
        ALERT!!!
        Instance is not created from a Gold Image
        Image ID: %s
        Instance ID: %s
        Instance Type: %s
        Owner: %s
        Zone ID: %s
        VPC ID: %s
        """%(event_details['imageiD'], event_details['instanceId'], event_details['instanceType'], event_details['keyName'], event_details['availabilityZone'], event_details['vpcId'])
        send_email('Alert, Instance is not created from a Gold Image', info)

    if not event_details['instanceType'] == 't2.micro':
        print("Not a Free Tier Instance")
        info = """\
        ALERT!!!
        Instance is not a Free Tier Instance
        Image ID: %s
        Instance ID: %s
        Instance Type: %s
        Owner: %s
        Zone ID: %s
        VPC ID: %s
        """%(event_details['imageiD'], event_details['instanceId'], event_details['instanceType'], event_details['keyName'], event_details['availabilityZone'], event_details['vpcId'])
        send_email('Alert, Instance is not a Free Tier Instance', info)


def check_iam_role(role_data):
    role_event_details = {}
    role_event_details['awsRegion'] = str(role_data['awsRegion'])
    role_event_details['userName'] = str(role_data['userIdentity']['userName'])
    role_event_details['roleName'] = str(role_data['responseElements']['role']['roleName'])
    role_event_details['arn'] = str(role_data['responseElements']['role']['arn'])

    info = """\
    ALERT!!!
    New Role Created
    AWS Region: %s
    User: %s
    Role Name: %s
    ARN: %s
    """%(role_event_details['awsRegion'], role_event_details['userName'], role_event_details['roleName'], role_event_details['arn'])
    send_email('Alert, New Role Created', info)


def check_iam_user(user_data):
    user_event_data = {}
    user_event_data['awsRegion'] = str(user_data['awsRegion'])
    user_event_data['arn'] = str(user_data['responseElements']['user']['arn'])
    user_event_data['userId'] = str(user_data['responseElements']['user']['userId'])
    user_event_data['userName'] = str(user_data['responseElements']['user']['userName'])

    info = """\
    ALERT!!!
    New User Created
    AWS Region: %s
    ARN: %s
    User Id: %s
    User Name: %s
    """%(user_event_data['awsRegion'], user_event_data['arn'], user_event_data['userId'], user_event_data['userName'])
    send_email('Alert, New User Created', info)



def send_email(subject, info):
    response = ses_client.send_email(
        Source='',
        Destination={
            'ToAddresses': [
                '',
                ''
            ],
            'CcAddresses': [
                '',
            ]
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': info
                }
            }
        }
    )
