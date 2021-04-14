import os
from enum import Enum, auto

import boto3


class FileSaver:

    class Mode(Enum):
        S3 = auto()
        LOCAL = auto()

    def __init__(self):
        self.file_saver = None

    def init_app(self, app):
        static_storage = app.config["STATIC_DATA_STORAGE"]

        if static_storage == "S3":
            self.file_saver = S3FileSaver(
                bucket_name=app.config["S3_BUCKET_NAME"],
                storage_path=app.config["S3_IMAGES_STORAGE_PATH"]
            )
        elif static_storage == "LOCAL":
            self.file_saver = LocalFileSaver(
                storage_path=app.config["IMAGE_UPLOADS"]
            )
        else:
            raise Exception("FileSaver Init Error, check storage config")

    def save_file(self, file, filename):
        try:
            self.file_saver.save_file(
                file=file,
                filename=filename
            )
        except Exception as e:
            print(e)
            raise Exception("An error occur while storing file")


class S3FileSaver:
    def __init__(self, bucket_name, storage_path):
        self.s3_client = boto3.client("s3")
        self.bucket_name = bucket_name
        self.storage_path = storage_path

    def save_file(self, file, filename):
        self.s3_client.upload_fileobj(
            file.stream,
            self.bucket_name,
            self.storage_path+filename,
            ExtraArgs={'ACL': 'public-read'}
        )


class LocalFileSaver:
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def save_file(self, file, filename):
        file.filename = filename
        file.save(
            os.path.join(self.storage_path, filename)
        )
