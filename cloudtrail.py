import gzip
import json
from pprint import pprint


us_west2_ami = ['ami-2e84611d', 'ami-06846135', 'ami-ed9b8bdd', 'ami-d52227e5', 'ami-25190415']
us_east1_ami = ['ami-895617ec', 'ami-0956176c', 'ami-47a0272c', 'ami-edcba488']

def download_json_file():
    with open('s3_test.json', 'rb') as f:
        data = json.load(f)
        pprint(data)
        # totalRecords=len(data["Records"])-1

        for details in data['Records']:
            if details['eventSource'] == 'ec2.amazonaws.com':
                 if details['eventName'] == 'RunInstances':
                     #pprint(details)
                    check_ec2(details)
            if details['eventSource'] == 'iam.amazonaws.com':
                 if details['eventName'] == 'CreateRole':
                     #pprint(details)
                    check_iam_role(details)
            if details['eventSource'] == 'iam.amazonaws.com':
                 if details['eventName'] == 'CreateUser':
                     #pprint(details)
                    check_iam_user(details)


def check_ec2(ec2_data):
    # pprint(i)
    ec2_event_details = {}
    ec2_event_details['imageiD'] = str(ec2_data['responseElements']['instancesSet']['items'][0]['imageId'])
    ec2_event_details['instanceId'] = str(ec2_data['responseElements']['instancesSet']['items'][0]['instanceId'])
    ec2_event_details['instanceType'] = str(ec2_data['responseElements']['instancesSet']['items'][0]['instanceType'])
    ec2_event_details['keyName'] = str(ec2_data['responseElements']['instancesSet']['items'][0]['keyName'])
    ec2_event_details['availabilityZone'] = str(ec2_data['responseElements']['instancesSet']['items'][0]['networkInterfaceSet']['items'][0]['availabilityZone'])
    ec2_event_details['vpcId'] = str(ec2_data['responseElements']['instancesSet']['items'][0]['networkInterfaceSet']['items'][0]['vpcId'])
    pprint(ec2_event_details)
    #pprint(i['responseElements']['instancesSet']['items'][0]['networkInterfaceSet']['items'][0])

    if not (ec2_event_details['imageiD'] in us_west2_ami or ec2_event_details['imageiD'] in us_east1_ami):
        print("Not a Gold Image")
    if not ec2_event_details['instanceType'] == 't2.micro':
        print("Not a Free Tier Instance")
    print "End of Records"


def check_iam_role(role_data):
    role_event_details = {}
    role_event_details['awsRegion'] = str(role_data['awsRegion'])
    role_event_details['userName'] = str(role_data['userIdentity']['userName'])
    role_event_details['roleName'] = str(role_data['responseElements']['role']['roleName'])
    role_event_details['arn'] = str(role_data['responseElements']['role']['arn'])
    pprint(role_event_details)
    print("\n")


def check_iam_user(user_data):
    user_event_data = {}
    user_event_data['awsRegion'] = str(user_data['awsRegion'])
    user_event_data['arn'] = str(user_data['responseElements']['user']['arn'])
    user_event_data['userId'] = str(user_data['responseElements']['user']['userId'])
    user_event_data['userName'] = str(user_data['responseElements']['user']['userName'])
    pprint(user_event_data)
    print("\n")
    pprint(user_data)



download_json_file()









# def download_json_file(bucket, key, download_path):
#     s3_client.download_file(bucket, key, download_path)
#     with gzip.open(download_path, 'rb') as f:
#         data = json.load(f)
#         totalRecords=len(data["Records"])-1
#         while totalRecords >0:
#             if data["Records"][totalRecords]["eventSource"] == "ec2.amazonaws.com":
#                 if data["Records"][totalRecords]["eventName"] == "RunInstances":
#                     print "Records Number is {}".format(totalRecords)
#                     print" Even Source is {}".format(data["Records"][totalRecords]["eventSource"])
#                     print "instance is {}".format(data["Records"][totalRecords]["responseElements"]["instancesSet"]["items"][0]["instanceId"])
#                     totalRecords = totalRecords - 1
#                     continue
#                 totalRecords = totalRecords - 1
#                 continue
#             totalRecords = totalRecords - 1
#         print "End of Records"