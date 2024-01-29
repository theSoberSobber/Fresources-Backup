from catbox import Uploader

class CatboxUploader:
    def __init__(self, token=''):
        self.uploader = Uploader(token=token)

    def upload_single_file(self, file_path):
        """
        Upload a single file to Catbox.

        :param file_path: Path to the file to be uploaded.
        :return: Catbox upload response.
        """
        file_type = file_path.split('.')[-1]
        upload = self.uploader.upload(file_type=file_type, file_raw=open(file_path, 'rb').read())
        return upload

    def upload_multiple_files(self, file_paths):
        """
        Upload multiple files to Catbox.

        :param file_paths: List of file paths to be uploaded.
        :return: List of Catbox upload responses.
        """
        log = []
        for file_path in file_paths:
            file_type = file_path.split('.')[-1]
            upload = self.uploader.upload(file_type=file_type, file_raw=open(file_path, 'rb').read())
            log.append(upload)
        return log