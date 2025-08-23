import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional, BinaryIO
import logging
import os
import secrets

logger = logging.getLogger(__name__)

class S3Handler:
    """Handler for AWS S3 operations"""
    
    def __init__(self):
        try:
            self.region = os.getenv('AWS_REGION', 'us-east-1')
            self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
            
            # Sprawdzenie, czy kluczowe zmienne są ustawione
            if not all([os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY'), self.bucket_name]):
                raise ValueError("Brakujące zmienne środowiskowe dla AWS S3")

            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=self.region
            )
            logger.info("S3 client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            self.s3_client = None
            self.bucket_name = None
    
    def upload_file(self, file_obj: BinaryIO, folder: str, original_filename: str) -> Optional[str]:
        """
        Przesyła plik do S3, nadaje mu unikalną nazwę i zwraca jego publiczny URL.
        """
        if not self.s3_client or not self.bucket_name:
            logger.error("S3 client not properly configured")
            return None
        
        try:
            # Tworzenie unikalnej nazwy pliku, aby uniknąć konfliktów
            file_extension = original_filename.split('.')[-1]
            random_key = secrets.token_hex(16)
            s3_key = f"{folder}/{random_key}.{file_extension}"
            
            # Przesyłanie pliku
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, s3_key)
            
            # Konstruowanie i zwracanie publicznego URL
            file_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
            logger.info(f"Successfully uploaded {s3_key} to S3. URL: {file_url}")
            return file_url
        except (ClientError, NoCredentialsError) as e:
            logger.error(f"Failed to upload file to S3: {e}")
            return None