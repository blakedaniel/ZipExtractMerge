# ZipExtractMerge
Extract multiple zip files and compile files into shared folder names

# Example Google Data Download Use Case
Google Takeout allows you to download all of your data from Google.  This is great, but it is a pain to download all of the files individually.  This script will extract all of the zip files and compile the files into a shared folder structure. This makes it easier to reupload the data to another service.

# Documentation
*Requirements:*
* Python 3.6+
* macOS or Linux for command line usage

## Class.zipExtractMerge
This class is used to extract all zip files in a directory into a destination directory. The constructor takes in the location of the zip files 'zip_directory' and the destination directory 'dest_directory'. It will then create the destination directory if it does not exist, and then extract all zip files into it, while sorting files into similar folders.

### args
- zip_directory (str): directory where zip files are
- dest_directory (str): directory to extract to

## Methods
### map_files(skip_types:list[str]=[])
Creates a dictionary of all files in the zip files and sets the obj.file_map attribute to it. The dictionary is structured as follows:
        
     obj.file_map {zip_file_path: {file_dir_path: {files}}}

#### args
- skip_types (list[str]): list of file types to skip

### extract_files(delete:bool=False)
Extracts all files in the zip files to the destination directory. If 'delete' is True, it will delete the zip files after extraction.

#### args
- delete (bool): When 'True' deletes each zip file after extraction. Default: 'False'

## command line usage
execute by running the following command in the terminal:
./zipExtractMerge.py [zip_direct] [dest_direct] [skip_types] [delete]

#### args
- '-zd', '--zip_direct' (str): directory where zip files are
- '-dd', '--dest_direct' (str): directory to extract to
- '-st', '--skip_types' (str): list of file types seperated by commas and space to skip
- '-d', '--delete' (bool): When 'True' deletes each zip file after extraction. Default: 'False'