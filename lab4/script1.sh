#!/bin/bash

#ensuring correct number of args
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <local_file> <s3_bucket> <expiration_seconds>"
    exit 1
fi

#assign args to vars
LOCAL_FILE=$1
BUCKET_NAME=$2
EXPIRATION=$3

# Check if file exists
FILE_NAME=$(basename "$LOCAL_FILE")

#upload file to s3 bucket
echo "Uploading $LOCAL_FILE to s3://$BUCKET_NAME/"
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET_NAME/" --acl private

# Check if upload was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to upload file."
    exit 1
fi

#create presigned url
echo "Generating presigned URL for $FILE_NAME with expiration: $EXPIRATION seconds"
PRESIGNED_URL=$(aws s3 presign "s3://$BUCKET_NAME/$FILE_NAME" --expires-in "$EXPIRATION")

#output url
echo "Presigned URL: $PRESIGNED_URL"