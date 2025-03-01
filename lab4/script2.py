import argparse
import boto3
import requests
import os
import sys

def download_file(url, save_path):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Downloaded file: {save_path}")
    else:
        sys.exit(1)

def upload_to_s3(bucket_name, local_file, s3_file_name):
    #upload file to s3
    s3 = boto3.client('s3')
    
    s3.upload_file(local_file, bucket_name, s3_file_name)
    print(f"Uploaded {local_file} to s3://{bucket_name}/{s3_file_name}")

def generate_presigned_url(bucket_name, s3_file_name, expiration):
    #creating presigned url
    s3 = boto3.client('s3')
    
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': s3_file_name},
        ExpiresIn=expiration
    )
    return presigned_url

def main():
    parser=argparse.ArgumentParser(description="Download a file, upload it to S3, and generate a presigned URL")
    parser.add_argument("url", help="URL of the file to download")
    parser.add_argument("bucket", help="S3 bucket name")
    parser.add_argument("expiration", type=int, help="Presigned URL expiration time in seconds")

    args = parser.parse_args()

    file_name = os.path.basename(args.url)
    download_file(args.url, file_name)

    upload_to_s3(args.bucket, file_name, file_name)

    presigned_url = generate_presigned_url(args.bucket, file_name, args.expiration)
    print(f"Presigned URL (expires in {args.expiration} seconds):\n{presigned_url}")

if __name__ == "__main__":
    main()
