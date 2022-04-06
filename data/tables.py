import boto3

creds = open('.creds').read().split('\n')

ddb = boto3.resource('dynamodb',
    aws_access_key_id=creds[0],
    aws_secret_access_key=creds[1],
    region_name=creds[2])

streams_table = ddb.Table('streamy_streams')
posts_table = ddb.Table('streamy_posts')


def get_streams_table():
    return streams_table


def get_posts_table():
    return posts_table
