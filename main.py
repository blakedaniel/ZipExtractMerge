from zipfile import ZipFile
from collections import defaultdict
from itertools import count
from datetime import datetime
import argparse
import os

# /Users/blakevanfleteren/Documents/for_extraction
# /Users/blakevanfleteren/Programs/GitHub/zip_extract


class ZipMergeExtract:
    def __init__(self, zip_directory:str, dest_directory:str):
        """This class is used to extract all zip files in a directory into a 
        destination directory. The constructor takes in the location of the 
        zip files and the destination directory. It will then create the 
        destination directory if it does not exist, and then extract all zip 
        files into it, while sorting files into similar folders.

        Args:
            zip_directory (str): directory where zip files are
            dest_directory (str): directory to extract to
        """
        self.zip_direct = zip_directory
        self.dest_direct = f"{dest_directory}/{datetime.utcnow().date()}-extracted"
        self.files = os.listdir(self.zip_direct)
        self.files = [self.zip_direct + "/" + file 
                      for file in self.files if file != ".DS_Store"]
        os.mkdir(self.dest_direct)
        
    def map_files(self, skip_types:list[str] = []):
        """Creates a dictionary of all files in the zip files and sets the
        obj.file_map attribute to it. The dictionary is structured as follows:
        
        obj.file_map {zip_file_path: {file_dir_path: {files}}}

        Args:
            skip_types (list[str], optional): file types to be ignored. Defaults to [].
        """
        self.file_map = defaultdict(lambda: defaultdict(set))
        self.skips = {skip_type: 0 for skip_type in skip_types} 
        for file in self.files:
            with ZipFile(file, 'r') as zip:
                members = zip.namelist()
                for member in members:
                    dir_path = member.split("/")
                    file_name = dir_path.pop()
                    file_type = file_name.split(".")[-1]
                    if file_type in skip_types:
                        self.skips[file_type] += 1
                        continue
                    dir_path = "/".join(dir_path)
                    self.file_map[file][dir_path].add(file_name)
    
    def _batch_delete(self, files:list[str]):
        for file in files:
            os.remove(file)
    
    def extract_files(self, delete:bool=False):
        """Extracts all files in the zip files into the destination directory.

        Args:
            delete (bool, optional): When True, zip file will be deleted after
            extraction. Defaults to False.
        """
        file_cnt = count(1)
        for file, cnt in zip(self.files, file_cnt):
            print(f"Working on: {file} ({cnt}/{len(self.files)})")
            ext_file = self.file_map[file]
            with ZipFile(file, 'r') as zip_file:
                for dir_path, files in ext_file.items():
                    if len(file) == 0:
                        continue
                    for member in files:
                        member = dir_path + "/" + member
                        zip_file.extract(member, self.dest_direct)
            if delete:
                self._batch_delete(file)

if __name__ == "__main__":
    ext_dir = input("Enter the directory of the zip files: ")
    dest_dir = input("Enter the directory to extract to: ")
    parser = argparse.ArgumentParser()
    parser.add_argument('-zd', '--zip_dir',
                        help='path of folder where zip files are',
                        type=str, default='~/Documents/for_extraction')
    parser.add_argument('-dd', '--dest_dir',
                        help='path of folder where zip files are',
                        type=str, default='~/Documents/')
    parser.add_argument('-st', '--skip_types',
                        help='file types to skip sperated by commas (e.g. json, docx, etc.)',
                        type=str, default='')
    parser.add_argument('-d', '--delete',
                        help='delete zip files after extraction (True/False)',
                        type=bool, default=False)
    args = parser.parse_args()
    skip_types = args.skip_type.split(", ")
    obj = ZipMergeExtract(args.zip_dir, args.dest_dir)
    obj.map_files(skip_types=skip_types)
    obj.extract_files(args.delete)
