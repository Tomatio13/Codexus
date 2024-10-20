import os
import csv
import re
import shutil
import base64
import logging
import yaml

logger = logging.getLogger(__name__)

class FileManager:
    def __init__(self, config):
        self.config = config

    def create_file(self, path: str, content: str) -> None:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as file:
                file.write(content)
            logger.info(f"File saved at: {path}")
        except Exception as e:
            logger.error(f"Error saving file at {path}: {e}")

    def read_requirements(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            logger.error(f"The file at path {file_path} does not exist.")
            raise FileNotFoundError(f"The file at path {file_path} does not exist.")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            logger.error(f"An error occurred while reading the file at {file_path}: {e}")
            raise IOError(f"An error occurred while reading the file at {file_path}: {e}")

    def get_binary_file_downloader_html(self, bin_file: str) -> str:
        try:
            file_label = os.path.basename(bin_file)
            with open(bin_file, 'rb') as f:
                data = f.read()
                bin_str = base64.b64encode(data).decode()
                href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
                return href
        except IOError as e:
            logger.error(f"Error reading file {bin_file}: {e}")
            return None
        
    def get_extention_language_mapping(self):
        csv_file_path = self.config['extension_mapping']
        extension_to_language = {}
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    extension = row.get('extension')
                    language = row.get('language')
                    extension_to_language[extension] = language
            logger.info(f"Loaded extension to language mapping from {csv_file_path}")
            return extension_to_language
        except IOError as e:
            logger.error(f"Error reading file {csv_file_path}: {e}")
            return None

    def replace_headings(self, markdown_text):
        try:
            markdown_text = re.sub(r'(?m)^# ', '## ', markdown_text)
            markdown_text = re.sub(r'(?m)^## ', '### ', markdown_text)
            markdown_text = re.sub(r'(?m)^### ', '#### ', markdown_text)
            logger.info("Replaced headings in markdown text")
            return markdown_text
        except Exception as e:
            logger.error(f"Error replacing headings in markdown text: {e}")
            return markdown_text

    def zip_folder(self, folder_path, output_path):
        try:
            shutil.make_archive(output_path, 'zip', folder_path)
            logger.info(f"Folder {folder_path} zipped successfully to {output_path}.zip")
        except Exception as e:
            logger.error(f"Error zipping folder {folder_path}: {e}")

    def delete_folder(self, folder_path):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                shutil.rmtree(folder_path)
                logger.info(f"Folder '{folder_path}' has been deleted successfully.")
            except Exception as e:
                logger.error(f"Error deleting folder {folder_path}: {e}")
        else:
            logger.warning(f"Folder '{folder_path}' does not exist.")
