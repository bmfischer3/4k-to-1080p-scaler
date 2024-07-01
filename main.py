import logging
import sys
import ffmpeg
import shutil
from pathlib import Path
from dotenv import load_dotenv
import subprocess
import prettyprint
import os
import hashlib

# Load envrionment variables from .env file. 
load_dotenv()

# Get values of the environment variables
original_file_path = os.getenv("ORIGINAL_FILE_PATH")
temp_file_path = os.getenv("TEMP_FILE_PATH")
feature_check_high_def = bool(os.getenv("FEATURE_CHECK_HIGH_DEF"))
feature_run_main = bool(os.getenv("FEATURE_RUN_MAIN"))


# Globals

file_name_list = []
file_path_list = []
dest_filepath_list = []
combined_list = []

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main(file_path_list: list):

    # feature flag

    if feature_run_main == True:

        # Create the path for the destination file
        dest_folder = temp_file_path

        for file in file_name_list:
            dest_path = dest_folder + "/" + file
            dest_filepath_list.append(dest_path)

        # Zip the lists

        combined_list_zipped = list(zip(file_path_list,dest_filepath_list))

        for og_path, dest_path in combined_list_zipped:
            # Create a copy of the original file in the temporary directory. 
            shutil.copy2(og_path, dest_path)

            # Get the size of each file in bytes and check the original and new copy match. 
            original_file_hash = md5(og_path)
            copied_file_hash = md5(dest_path)

            if original_file_hash == copied_file_hash:
            
                # Start converting the copied file. 
                convert_to_1080p(dest_path)
                file_name = os.path.basename(og_path).split('/')

                og_file_name = file_name[0].split('.')
                file_ext = '.' + og_file_name[-1]

                # The below variable creates the path name for where the converted 1080p file will live in the temporary directory. 
                converted_path = '/'.join(str(x) for x in (os.path.abspath(dest_path)).split('/')[:-1]) + '/' + og_file_name[0] + '_1080p' + file_ext

                # The below is the 1080p path where the 1080p file will go into the original 4k file's directory. 
                og_directory_1080_path = '/'.join(str(x) for x in (os.path.abspath(og_path)).split('/')[:-1]) + '/' + og_file_name[0] + '_1080p' + file_ext


                # Verify the converted file is in 1080p. 
                if check_standard_def(converted_path) == True:

                    # Copy the converted 1080p file to the original 4k file's directory. 
                    shutil.copy2(converted_path, og_directory_1080_path)

                    # Verify the converted file was correctly copied to the original 4k file's directory. 

                    converted_file_copy_hash = md5(converted_path)
                    converted_file_og_hash = md5(og_directory_1080_path)

                    # TODO: hashing check
                    if converted_file_copy_hash == converted_file_og_hash:
                        print("Converted file in the temp directory and converted file in the original directory match")

                        # Delete the converted copy in the temp directory
                        os.remove(converted_path)

                        # Delete the 4k copy in the temp directory
                        os.remove(dest_path)

                        # Delete the 4k original in the origin directory
                        os.remove(og_path)

                        print(f"Success in converting and removing files for {og_file_name[0]}.")
                    else:
                        print("Converted files do not match. There was an error.")
            else:
                print(f"Files are not the same. {og_path} and {dest_path} are the issues.")

    else:
        print("Feature flag is turned off for main.")



def md5(file_name: str) -> str:
    # https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_standard_def(converted_path: str) -> bool:
    """Checks the provided file path to verify the converted file is 1920 x 1080 resolution. 

    Args:
        converted_path (_str_): File path as a string for where the converted video file resides. 

    Returns:
        bool: _descri
    """
    #TODO: error handling
    probe = ffmpeg.probe(converted_path)
    width = probe['streams'][0]['width']
    height = probe['streams'][0]['height']
    if width == 1920:
        if height == 1080:
            print(f'Return True - {converted_path} is 1920x1080')
            return True
        else:
            print(f'Return False - {converted_path} is not 1920x1080')
            return False
    else:
        print(f'Return False - {converted_path} is not 1920x1080')
        return False



def check_high_def(original_path: str) -> bool:
    """ Check the resolution of file and returns true if in 3840 x 2160

    Args:
        original_path (_str_): Path name to video file as a string. 

    Returns:
        bool: Returns true if the file is in a 4k resolution, 3840 x 2160
    """
    try:

        probe = ffmpeg.probe(original_path)

        # Get the height and width from the returned json data in ffmpeg.probe. 
        width = probe['streams'][0]['width']
        height = probe['streams'][0]['height']

        # check the width and height. 
        # Feature Flag

        if feature_check_high_def == True:
            if width >= 3840 and height >= 2160:
                print(f'Return True - {original_path} is 3840 x 2160')
                return True
            else:
                print(f'Return False - {original_path} is not 3840 x 2160')
                return False
        else:
            print("Feature flag for checking high defintiion 4k video is off.")
        

    except ffmpeg.Error as ex:
        logging.info("error with gathering video info %s", ex)



def get_original_file_paths(original_file_path: str) -> list:
    """_summary_

    Args:
        origin_file_path (_str_): The directory path within your system for where the original 4k files reside.

    Returns:
        list: Returns a single list with paths of each 4k file in the directory for .mp4, .MP4, .mov, and .MOV files. 
    """
    for i in os.listdir(original_file_path):

        # Get the path of each file in the directory. 
        filename = os.path.basename(i)
        filepath = str(original_file_path) + i
        
        # Check the video file extension.  

        if filename.lower().endswith('.mp4') or filename.lower().endswith('.mov'):

        # Check the video resoloution and verify it's a 4k file. 

            if check_high_def(filepath) == True:
                file_name_list.append(filename)
                file_path_list.append(filepath)
                
    return file_path_list



def convert_to_1080p(path_copy: str) -> str:
    """_summary_

    Args:
        path_copy (_str_): File path for the 4k copy in the temporary directory. 

    Returns:
        str: Returns the path of the 1080p copy in the temporary directory as a string. 
    """
    file_copy_name = (os.path.basename(path_copy).split('/')[-1]).split('.')[0]
    file_ext = '.'+(os.path.basename(path_copy).split('/')[-1]).split('.')[1]
    path_copy_name = '/'.join(str(x) for x in (os.path.abspath(path_copy).split('/')[:-1]))
    conversion = subprocess.run(
        [
            'ffmpeg',
            '-i', 
            path_copy,
            '-vf',
            'scale=1920:1080',
            '-c:a', 
            'copy',
            path_copy_name + '/' + file_copy_name + '_1080p' + file_ext,
            ]
            )
    
    return conversion

a = main(get_original_file_paths(original_file_path))