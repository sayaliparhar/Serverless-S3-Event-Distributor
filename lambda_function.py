import boto3
import json

def lambda_handler(event, context):
    # 1. Extract info from the S3 Event
    # Note: 'name' is the dictionary key, NOT your specific bucket name.
    bucket = event['Records'][0]['s3']['bucket']['name'] 
    key = event['Records'][0]['s3']['object']['key']
    size = event['Records'][0]['s3']['object']['size']

    # 2. Create a message
    # We use the variable 'bucket' which now holds your bucket name
    message = f"New file uploaded!\nBucket: {bucket}\nFile: {key}\nSize: {size} bytes"

    # 3. Send to SNS
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:ap-south-1:861276090426:s3-upload-notify-topic',
        Subject='S3 Upload Alert',
        Message=message
    )
    
    return {'statusCode': 200, 'body': 'Notification Sent!'}