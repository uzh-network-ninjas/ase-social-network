#!/bin/bash
echo "Initializing localstack s3"

awslocal s3 mb s3://ms-user
awslocal s3 mb s3://ms-review
# awslocal sqs create-queue --queue-name my-app-queue
# awslocal ses verify-email-identity --email-address app@demo.com