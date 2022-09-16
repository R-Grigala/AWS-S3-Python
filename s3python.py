import boto3
from decouple import config
import os

BUCKET_NAME = "smartbucket-ofdigtal"
BUCKET_REGION = "us-east-1"

def s3_client_connect():
    
    s3_client = boto3.client("s3",
                            aws_access_key_id=config('aws_access_key_id'),
                            aws_secret_access_key=config('aws_secret_access_key')
    )

    return s3_client

def s3_resource_connect():

    s3_resource = boto3.resource('s3',
                            aws_access_key_id=config('aws_access_key_id'),
                            aws_secret_access_key=config('aws_secret_access_key')
    )

    return s3_resource

# -----------------------------------
# Create S3 Bucket using boto3
# -----------------------------------

def create_bucket(bucket_name,bucket_region = None):

    if bucket_region is None:
        s3_client_connect().create_bucket(Bucket=bucket_name)

    else:
        location = {'LocationConstraint': bucket_region}
        s3_client_connect().create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

    return "Bucket succesfully created !"

# -----------------------------------
# Empty S3 Bucket using boto3
# -----------------------------------

def empty_bucket(bucket_name):

    bucket = s3_resource_connect().Bucket(bucket_name)
    bucket.objects.all().delete()

    return "Bucket has been empty!"

# -----------------------------------
# Delete S3 Bucket using boto3
# -----------------------------------

def delete_bucket(bucket_name):

    bucket = s3_resource_connect().Bucket(bucket_name)
    bucket.delete()

    return "Bucket has been deleted!"


# -----------------------------------
# List all S3 Bucket using boto3
# -----------------------------------

def list_buckets():
    
    for bucket in s3_resource_connect().buckets.all():
        with open("OfDigital-Buckets.txt", "a") as f:
            f.write(f"{bucket.name}\n")

# -----------------------------------
# Upload file to S3 Bucket using boto3
# -----------------------------------

def upload_file(file_name, bucket_name, object_name = None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    response = s3_client_connect().upload_file(file_name, bucket_name, object_name)

    return "File Uploaded!"


# -----------------------------------
# Upload simple file to specific folder into S3 Bucket using boto3
# -----------------------------------

def upload_file_to_folder(file_name, bucket_name, folder_name, object_name = None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    response = s3_client_connect().upload_file(file_name, bucket_name, f"{folder_name}/{object_name}")

    return "File uploaded Succesfully!"


# -----------------------------------
# Download files from S3 Bucket using boto3
# -----------------------------------

def download_file(bucket_name, object_name, file_name):

    s3_client_connect().download_file(bucket_name, object_name, file_name)

    return "File downloaded!"

# -----------------------------------
# Read object from S3 Bucket using boto3
# -----------------------------------

def read_object(bucket_name, key):

    obj = s3_resource_connect().Object(bucket_name, key)

    return obj.get()['Body'].read().decode('utf-8')

# -----------------------------------
# Enable versioning for S3 Bucket using boto3
# -----------------------------------

def version_bucket_files(bucket_name):
    s3_client_connect().put_bucket_versioning(
        Bucket = bucket_name,
        VersioningConfiguration = {
            'Status': 'Enabled'

        }
    )

    return "versioning Enabled!"


# -----------------------------------
# Create S3 Web hosting using boto3
# -----------------------------------

def host_static_website(bucket_name):

    s3_resource_connect().create_bucket(Bucket=bucket_name)

    website_config = {
        "IndexDocument": {"Suffix": "index.html"},
        "ErrorDocument": {"Key": "error.html"},
    }

    s3_client_connect().put_bucket_website(
        Bucket = bucket_name,
        WebsiteConfiguration = website_config
    )

    index_file = os.path.basename("index.html")
    error_file = os.path.basename("error.html")
    s3_client_connect().put_object(Bucket=bucket_name, ACL="public-read", Key="index.html",
                                    Body=open(index_file).read(), ContentType="text/html")

    s3_client_connect().put_object(Bucket=bucket_name, ACL="public-read", Key="error.html",
                                    Body=open(error_file).read(), ContentType="text/html")

                        
    return "Static WebHosting Bucket Created!"


# -----------------------------------

if __name__ == '__main__':

    # n = int(input("How many Bucket to create: "))

    # for i in range(n):
        
    #     bname = input("Bucket Name: ")
    #     print(create_bucket(bname))
    

    # print(create_bucket(BUCKET_NAME))
    # print(empty_bucket(BUCKET_NAME))
    # print(delete_bucket(BUCKET_NAME))
    # list_buckets()

    # print(upload_file("OfDigitalUser.txt", BUCKET_NAME))

    # print(upload_file_to_folder("myfile.txt", BUCKET_NAME, "OfDigitalFolder"))

    # print(download_file(BUCKET_NAME, "SuperFile.txt", "mySuperFile.txt"))

    # print(read_object(BUCKET_NAME, "OfDigitalUser.txt"))
    # print(version_bucket_files(BUCKET_NAME))
    
    print(host_static_website("hostofdigital"))
