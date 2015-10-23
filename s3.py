__author__ = 'bwalke'
from boto.s3.connection import S3Connection

aws_connection = S3Connection()
bucket = aws_connection.get_bucket('')

for key in bucket.list():
        print "{name}\t{size}\t{modified}".format(
                name = key.name,
                size = key.size,
                modified = key.last_modified,
                )

# key = bucket.new_key('hello.txt')
# key.set_contents_from_string('Hello World!')
