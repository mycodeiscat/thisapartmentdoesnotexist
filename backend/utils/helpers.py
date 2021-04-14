import boto3, botocore
from .config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name, filename, content_type, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": content_type
            }
        )
        return "{}{}".format(S3_LOCATION, filename)
    except Exception as e:
        print("Exception:", e)
        return e
