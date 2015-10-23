__author__ = 'bwalke'
from pprint import pprint
import boto3
import boto.ses

ses_client = boto3.client('ses')
# conn = boto.ses.connect_to_region('us-west-2')

# conn.verify_email_address('bwalke@juniper.net')

# pprint(conn.list_verified_email_addresses())

# conn.send_email(
#         'bwalke@juniper.net',
#         'AMAZON email',
#         'test',
#         ['bwalke@juniper.net'])


def send_email(subject, info):
    response = ses_client.send_email(
        Source='',
        Destination={
            'ToAddresses': [
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


info = """\
    Image ID: %s
    Instance ID: %s
    Instance Type: %s
    Owner: %s
    Zone ID: %s
    VPC ID: %s
    """%('imageiD', 'instanceId', 'instanceType', 'keyName', 'availabilityZone', 'vpcId')


send_email('ec2_check', info)
