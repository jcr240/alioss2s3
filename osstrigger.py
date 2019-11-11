# -*- coding: utf-8 -*-
import oss2
import json
import boto3



def handler(event, context):
    """
    Replicate the object from OSS to s3.
    event:   The OSS event json string. Including oss object uri and other information.
    context: The function context, including credential and runtime info.
             For detail info, please refer to https://help.aliyun.com/document_detail/56316.html#using-context
    """
    evt_list = json.loads(event)
    creds = context.credentials
    auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)

    # Parse the event to get the source object info.
    evt = evt_list['events'][0]
    bucket_name = evt['oss']['bucket']['name']
    endpoint = 'oss-' + evt['region'] + '.aliyuncs.com'
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    object_name = evt['oss']['object']['key']
    print (object_name)
    # Download the oss object.
    remote_stream = bucket.get_object(object_name)
    if not remote_stream:
        raise RuntimeError('failed to get oss object. bucket: %s. object: %s' % (bucket_name, object_name))
    print 'download object from oss success: %s' % object_name
    content=remote_stream.read()
    # replicate to AWS S3
    S3_bucket_name='changeme'
    client = boto3.client('s3',aws_access_key_id='AK(changeme)',aws_secret_access_key='SK(changeme)',region_name='cn-north-1')
    #client.upload_file(object_name,S3_bucket_name,object_name)
    client.put_object(
        Bucket=S3_bucket_name,
        Key=object_name,
        Body=content
    )
