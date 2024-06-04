# csv data transform

This project demonstrates how to transform data from csv file ```field_of_study_exercise.csv ``` and output is a summary report on the data cleaning process (e.g., number of
missing values removed, mapping ratio)

Run app : 
```bash
python transform.py
```
All the output records will be stored in AWS S3. We will use SQS and AWS Lambda function to get notification and file transformed whenever files received. 

## Get Event Notification by SQS, Lambda and write to AWS S3 bucket 
There are 5 steps: 
- We have Lead, Persona and transformed csv data written to a landing S3 bucket, named ```dev-data-external-land-ap-southeast-1 ```
- Create Event Notification in the landing S3 bucket in order to receive message from SQS whenever new event written to the S3. 
- Create another targeting S3 bucket, named ```dev-data-external-target-ap-southeast-1 ``` 
- Create an Access policy (Permissions) on SQS associated with the landing S3 bucket. The Access Policy should be like this : 
```bash 
{
  "Version": "2012-10-17",
  "Id": "example-ID",
  "Statement": [
    {
      "Sid": "example-statement-ID",
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": "SQS:SendMessage",
      "Resource": "arn:aws:sqs:ap-southeast-1:261858807236:dev-data-s3ToSqsTest",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "261858807236"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:::dev-data-external-land-ap-southeast-1"
        }
      }
    }
  ]
} 
```
- Authorized approriate IAM Policies for S3, Cloudwatch, SQS and Lambda function in order to read-write to S3 bucket
The Policies JSON should look like this : 
```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sqs:DeleteMessage",
                "sqs:GetQueueUrl",
                "sqs:ReceiveMessage",
                "sqs:SendMessage",
                "sqs:GetQueueAttributes",
                "logs:CreateLogGroup",
                "logs:PutLogEvents",
                "logs:CreateLogStream",
                "sqs:DeleteQueue",
                "sqs:CreateQueue",
                "s3:ListAccessPoints",
                "s3:ListAccessPointsForObjectLambda",
                "s3:ListBucket",
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "sqs:SetQueueAttributes",
                "sns:Publish",
                "sns:ListTopics",
                "sns:CreateTopic",
                "sns:Subscribe",
                "s3:CreateBucket"
            ],
            "Resource": [
                "arn:aws:sqs:ap-southeast-1:261858807236:dev-data-s3ToSqsTest",
                "arn:aws:logs:*:*:*",
                "arn:aws:s3:::arn:aws:s3:::dev-datar-external-land-ap-southeast-1",
                "arn:aws:s3:::dev-datar-external-target-ap-southeast-1",
                "arn:aws:sqs:ap-southeast-1:261858807236:dev-data-s3ToSqsTest"
            ]
        },
        {
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::arn:aws:s3:::dev-data-external-land-ap-southeast-1",
                "arn:aws:s3:::arn:aws:s3:::dev-data-external-land-ap-southeast-1/data_competitor/*",
                "arn:aws:s3:::dev-data-external-target-ap-southeast-1",
                "arn:aws:s3:::dev-data-external-target-ap-southeast-1/data_competitor/*"
            ],
            "Effect": "Allow",
            "Sid": "WriteAccessForS3"
        }
    ]
}

```
After finishing setting up, Lambda function will trigger automatically and write to target S3 bucket. 
