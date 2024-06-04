import json
import boto3
import logging
import datetime
import re
import time
from server.model.transform import cleaned_data, summary


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients and resources
env = 'dev'
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

queue_url_response = sqs.get_queue_url(QueueName=f'{env}-data-s3ToSQS-demo')
queue_url = queue_url_response['QueueUrl']
landing_bucket = 'dev-data-external-land-ap-southeast-1'
target_bucket = 'dev-data-external-target-ap-southeast-1'

def delete_sqs_message(event):
    # get receipt handle to ensure correct deletion 
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
    messages = response.get('Messages', [])
    if messages: 
        receipt_handle = messages[0]['ReceiptHandle']  # Adjusted to get the first message's receipt handle
        delete_response = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    else: 
        print("No messages available in the queue.")
    

def handle_missing_fields(json_object):
    fields = ['level', 'level_name', 'field_of_study', 'academic_field']
    
    # data = {}
    for field in fields:
        if json_object.get(field) is None:  # Check if the field value is None
            cleaned_data[field] = None
        else:
            cleaned_data[field] = json_object.get(field, None)  # Get the field value, or return None if missing
    
    return cleaned_data, summary


def lambda_handler(event, context):
    # startTime and endTime used to check if exceed 10 minutes, exit the lambda function
    startTime = time.time()
    endTime = time.time()
    payloads = event.get('Records')
    if payloads:
        data_list = []  # Initialize data list outside the loop
        for e in payloads:
            body = e.get('body')
            if body is not None:
                parameters = json.loads(body)
                try:
                    s3Bucket = parameters["Records"][0]["s3"]["bucket"]["name"]
                    s3ObjectKey = parameters["Records"][0]["s3"]["object"]["key"]
                    response = s3.get_object(Bucket=landing_bucket, Key=s3ObjectKey)
                    content = response['Body'].read().decode('utf-8')
                    for line in content.split('\n'):
                        if line.strip():
                            json_object = json.loads(line)

                            # Extract all data from JSON object
                            cleaned_data = handle_missing_fields(json_object)  # Use the modified function
                            # print("data:",data)
                            
                            
                except KeyError as e:
                    logger.error("KeyError: %s", e)
            else:
                logger.error("Body is None for event: %s", e)
            endTime = time.time()  # Update endTime inside the loop
    else:
        print("No event available in the queue.")
    
    # Write all data to a single file
    s3_prefix = f'data/'
    date_today = datetime.datetime.now() + datetime.timedelta(hours=8)
    d1 = date_today.strftime("%Y%m%d")
    exported_date_path = "exported_date=" + d1 + "/"
    folder_path = s3_prefix + exported_date_path  + "data_competitor.json"
   
    s3.put_object(Bucket=target_bucket, Key=folder_path, Body=json.dumps(cleaned_data))
    s3.put_object(Bucket=target_bucket, Key=folder_path, Body=json.dumps(summary))
    print(f"Ingesting to {target_bucket}/{folder_path}")
    print(f"Ingestion success with {summary}!")
    
  
    # Delete message from queue after processing
    delete_sqs_message(e)
