import datetime
import os
from concurrent.futures import ThreadPoolExecutor

from google.cloud import storage
from google.cloud.storage import Blob, Bucket
from .credentials import get_credentials


class GCS:
    def __init__(self, service_account: str | dict = None):
        service_account_credentials = get_credentials(service_account)
        if service_account_credentials:
            self.storage_client = storage.Client(credentials=service_account_credentials)
        else:
            self.storage_client = storage.Client()

    def get_blob(self, bucket_name, destination_blob_name) -> Blob:
        bucket: Bucket = self.storage_client.bucket(bucket_name)
        return bucket.blob(destination_blob_name)

    def upload_stream(self, bucket_name, destination_blob_name, iter):
        blob: Blob = self.get_blob(bucket_name, destination_blob_name)
        with blob.open('wb', timeout=60000 * 60) as f:
            for chunk in iter:
                f.write(chunk)

    def upload(self, bucket_name, destination_blob_name, file_obj):
        self.get_blob(bucket_name, destination_blob_name).upload_from_string(file_obj)

    def upload_from_filename(self, bucket_name, destination_blob_name, local_file_path):
        self.get_blob(bucket_name, destination_blob_name).upload_from_filename(local_file_path)

    def generate_signed_url(self, bucket_name, blob_name, expiration=30, content_type=None):
        """
        为 GCS 中的任何文件类型生成签名 URL

        参数:
            bucket_name (str): GCS 存储桶名称
            blob_name (str): 对象名称/路径
            expiration (int): URL 有效期（分钟），默认 30 分钟
            content_type (str, optional): 指定内容类型，如果为 None 则自动检测
        返回:
            str: 签名 URL
        """
        blob = self.get_blob(bucket_name, blob_name)
        filename = blob_name.split("/")[-1]
        # 如果未指定内容类型，则根据文件扩展名自动检测
        if content_type is None:
            file_extension = os.path.splitext(filename)[1].lower()
            content_type_map = {
                '.txt': 'text/plain',
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.json': 'application/json',
                '.xml': 'application/xml',
                '.pdf': 'application/pdf',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.xls': 'application/vnd.ms-excel',
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.ppt': 'application/vnd.ms-powerpoint',
                '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
                '.webp': 'image/webp',
                '.mp4': 'video/mp4',
                '.webm': 'video/webm',
                '.mov': 'video/quicktime',
                '.avi': 'video/x-msvideo',
                '.wmv': 'video/x-ms-wmv',
                '.mp3': 'audio/mpeg',
                '.wav': 'audio/wav',
                '.ogg': 'audio/ogg',
                '.zip': 'application/zip',
                '.rar': 'application/x-rar-compressed',
                '.tar': 'application/x-tar',
                '.gz': 'application/gzip',
                '.csv': 'text/csv',
                '.md': 'text/markdown',
            }
            content_type = content_type_map.get(file_extension, 'application/octet-stream')
            if blob.content_type:
                content_type = blob.content_type

        disposition = f'attachment; filename="{filename}"'
        expiration_delta = datetime.timedelta(minutes=expiration)
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=expiration_delta,
            method="GET",
            response_disposition=disposition,
            response_type=content_type
        )
        return signed_url

    def file_exists(self, bucket_name, destination_blob_name) -> bool:
        bucket: Bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.get_blob(destination_blob_name)
        return blob is not None

    def upload_folder(self, bucket_name, folder_path, file_prefix):
        gcs_file_path = []
        with ThreadPoolExecutor() as executor:
            futures = []
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    local_file_path = os.path.join(root, file_name)
                    gcs_blob_name = f"{file_prefix}/{file_name}"
                    gcs_file_path.append(f"gs://{bucket_name}/{gcs_blob_name}")
                    futures.append(
                        executor.submit(self.upload_from_filename, bucket_name, gcs_blob_name, local_file_path))
            for future in futures:
                future.result()
        return gcs_file_path

    def download_file(self, bucket_name, source_blob_name, destination_file_name):
        blob = self.get_blob(bucket_name, source_blob_name)
        blob.download_to_filename(destination_file_name)
        return destination_file_name

    def list_files(self, bucket_name):
        bucket = self.storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()
        return [i.name for i in blobs]
