__author__ = 'bwalke'
from pprint import pprint
import boto
import boto.ec2
import boto.iam
import boto3
conn = boto.ec2.connect_to_region('us-west-2')


reservations = conn.get_all_instances()
ec2_details = [i for r in reservations for i in r.instances]

for i in ec2_details:
    if(i.id == ''):
        print("Instance ID:", i.id)
        print("Region:", i.region)
        print("Image ID:", i.image_id)
        print("Instance Type:", i.instance_type)
