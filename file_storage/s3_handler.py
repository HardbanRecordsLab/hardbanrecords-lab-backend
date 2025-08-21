import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional, BinaryIO
import logging
import os

logger = logging.getLogger(__name__)

class S3Handler:
    """Handler for AWS S3 operations"""
    
    def __init__(self):
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )
            self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            self.s3_client = None
            self.bucket_name = None
    
    def upload_file(self, file_obj: BinaryIO, key: str, content_type: str = None) -> bool:
        """Upload a file to S3"""
        if not self.s3_client or not self.bucket_name:
            logger.error("S3 client not properly configured")
            return False
        
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, key, ExtraArgs=extra_args)
            logger.info(f"Successfully uploaded {key} to S3")
            return True
        except (ClientError, NoCredentialsError) as e:
            logger.error(f"Failed to upload {key} to S3: {e}")
            return False
    
    def download_file(self, key: str, file_obj: BinaryIO) -> bool:
        """Download a file from S3"""
        if not self.s3_client or not self.bucket_name:
            logger.error("S3 client not properly configured")
            return False
        
        try:
            self.s3_client.download_fileobj(self.bucket_name, key, file_obj)
            logger.info(f"Successfully downloaded {key} from S3")
            return True
        except ClientError as e:
            logger.error(f"Failed to download {key} from S3: {e}")
            return False
    
    def delete_file(self, key: str) -> bool:
        """Delete a file from S3"""
        if not self.s3_client or not self.bucket_name:
            logger.error("S3 client not properly configured")
            return False
        
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info(f"Successfully deleted {key} from S3")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete {key} from S3: {e}")
            return False
    
    def file_exists(self, key: str) -> bool:
        """Check if a file exists in S3"""
        if not self.s3_client or not self.bucket_name:
            return False
        
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False
    
    def get_file_url(self, key: str, expiration: int = 3600) -> Optional[str]:
        """Generate a presigned URL for a file"""
        if not self.s3_client or not self.bucket_name:
            return None
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL for {key}: {e}")
            return None