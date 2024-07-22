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

# Globals

file_name_list = []
file_path_list = []
dest_filepath_list = []
combined_list = []
finished_file_size = []


# Load static .env Variables

# Temp path is the directory for where files will be copied to and converted. 
temp_file_path = os.getenv("TEMP_FILE_PATH")

# This is where the original 4K files live. Currently the program will not pick up on subdirectories within this path. 
original_file_path = os.getenv("ORIGINAL_FILE_PATH")

class FeatureFlags:
    def __init__(self):
        # May want to implement additional checks shown here: https://stackoverflow.com/questions/63116419/evaluate-boolean-environment-variable-in-python
        # Retrieves the .env variable if present, else returns False, lowercases all and verifies one of the strings is a true value. 
        self.logging_enabled = os.getenv('LOGGING_ENABLED', 'False').lower() in ('true', 't', '1')

        self.feature_check_high_def_enabled = os.getenv("FEATURE_CHECK_HIGH_DEF_ENABLED").lower() in ('true', 't', '1')

        self.finished_file_size_enabled = os.getenv("GET_FINISHED_FILE_SIZE_ENABLED").lower() in ('true', 't', '1')


def setup_logger(name, log_file, level=logging.DEBUG):
    """To setup as many loggers as needed."""
    # Source: https://stackoverflow.com/questions/11232230/logging-to-two-files-with-different-settings 

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(fmt=' %(name)s :: %(levelname)-8s :: %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger




if __name__ == "__main__":

    flags = FeatureFlags()

    def is_logging_enabled():
        return flags.logging_enabled

    if is_logging_enabled():
        print("Logging is enabled")
    else:
        print("Logging is disabled")


    def is_feature_check_high_def_enabled():
        return flags.feature_check_high_def_enabled

    if is_feature_check_high_def_enabled():
        print("Feature check high def is enabled")
    else:
        print("Feature check highi def is not enabled")


    def is_finished_file_size_enabled():
        return flags.finished_file_size_enabled

    if is_finished_file_size_enabled():
        print("Finished file size is enabled.")
    else:
        print("Finished file size is not enabled.")
                    


    if is_logging_enabled() == True:
        logger = setup_logger("logger", "test_log.log", logging.DEBUG)
        logger.debug("Initial loogging file has been created.")

        file_error_logger = setup_logger("file_error_logger", "file_error_log_list.log", logging.DEBUG)
        file_error_logger.debug("File error logger file has been initiated.")
    else:
        print(f"Logging feature flag turned off. Review the .env file and set to true to enable logging.")



def convert_videos_main(origin_file_path: str) -> None:
    """_summary_ Converts files within the video path list from 4K to 1080p. 

    Args:
        origin_file_path (str): Provide a path to a directory for where video files in a .mp4 or .mov format live. 
    """
    
    logger.debug("Conversion functions have been initiated. Collecting file paths. ")

    file_path_list = get_original_file_paths(origin_file_path)

    # Create the path for the destination file
    dest_folder = temp_file_path

    for file in file_name_list:
        dest_path = dest_folder + "/" + file
        dest_filepath_list.append(dest_path)
        logger.debug(f"{dest_path} has been appended to the dest_filepath_list.")

    # Zip the lists
    combined_list_zipped = list(zip(file_path_list,dest_filepath_list))
    logger.debug("The original file path list and destination file path list have been zipped together.")

    for og_path, dest_path in combined_list_zipped:
        # Create a copy of the original file in the temporary directory. 
        shutil.copy2(og_path, dest_path)
        logger.debug(f"The {og_path} has been copied to the {dest_path}.")

        # Get the size of each file in bytes and check the original and new copy match. 
        original_file_hash = md5(og_path)
        logger.debug(f"The hash size of the original file: {og_path} is {original_file_hash}.")
        copied_file_hash = md5(dest_path)
        logger.debug(f"The hash size of the copied file: {dest_path} is {copied_file_hash}.")

        if original_file_hash == copied_file_hash:
            logger.info(f"The original file hash and copied file hash match. Conversion is starting for {og_path}")
        
            # Start converting the copied file. 
            convert_to_1080p(dest_path)
            file_name = os.path.basename(og_path).split('/')

            og_file_name = file_name[0].split('.')
            file_ext = '.' + og_file_name[-1]

            # The below variable creates the path name for where the converted 1080p file will live in the temporary directory. 
            converted_path = '/'.join(str(x) for x in (os.path.abspath(dest_path)).split('/')[:-1]) + '/' + og_file_name[0] + '_1080p' + file_ext

            # 1080p path where the 1080p file will go into the original 4k file's directory. 
            og_directory_1080_path_components = []

            # Break down the path of the oroginal 4k file into its individual components and add them to a list without the slashes.  
            for component in os.path.abspath(og_path).split('/')[:-1]:
                og_directory_1080_path_components.append(component)
            
            # Remove the blank space in the first part of the list. 
            og_directory_1080_path_components.remove('')


            # Append the "_1080p" annotation and file extension to the end of the list and then join everything to create a path string. 
            og_directory_1080_path_components.append(og_file_name[0] + '_1080p' + file_ext)
            og_directory_1080_path_string = '/' + os.path.join(*og_directory_1080_path_components)
            og_directory_1080_path = os.path.normpath(og_directory_1080_path_string)

            logger.info(f"Processing File: {og_directory_1080_path}")

            try:
                # If the below runs successfully, no exception block is executed. 
                # Verify the converted file is in 1080p. 
                if check_standard_def(converted_path) == True:

                    # Copy the converted 1080p file to the original 4k file's directory. 
                    logger.info(f"Attempting to copy the 1080p copy {converted_path} to the original 4k file's directory: {og_directory_1080_path}.")
                    shutil.copy2(converted_path, og_directory_1080_path)

                    converted_file_copy_hash = md5(converted_path)
                    converted_file_og_hash = md5(og_directory_1080_path)
                    
                    remove_duplicate_files(converted_file_copy_hash, converted_file_og_hash, converted_path, dest_path, og_path, og_file_name)
                    logger.info(f"{og_path} successfully converted and duplicates have been removed.")


                else:
                    file_error_logger.debug(f"There is an error with {converted_path}.")



            except OSError as e:
                logger.warning(f"An OSError issue has occurred for {og_file_name}. Continuing to verify the converted file was correctly copied to the original 4k file's directory. ")
                
                converted_file_copy_hash = md5(converted_path)
                converted_file_og_hash = md5(og_directory_1080_path)

                logger.debug(f"With OSError raised, The converted copy placed in the original 4k directory and the converted copy in the temprorary directory have the following hashes: {converted_file_og_hash}, {converted_file_copy_hash}")
                file_error_logger.debug(f"{e} raised for {og_file_name}.")
            
                remove_duplicate_files(converted_file_copy_hash, converted_file_og_hash, converted_path, dest_path, og_path, og_file_name)

            except Exception as e:
                logger.error(f"Some other error has occurred: {e}")
            
            else:
                # Else statement executes if the control flow leaves the try block, no exception was raised and no return, continue, or break statement was executed. 
                # The below code executes if the try clause executes without throwing an errory. 
                logger.info(f"else statement has executed.")

def remove_duplicate_files(converted_file_copy_hash: str, converted_file_og_hash: str, converted_path: str, dest_path: str, og_path: str, og_file_name:str) -> None:
    """_summary_ Removes the converted copy in temp dir, 4k copy in temp dir, and 4k original in origin dir after confirming the hashes of the converted copies in the temp and origin dir match. 

    Args:
        converted_file_copy_hash (str): MD5 hash of the 1080p file residing in the temp dir. 
        converted_file_og_hash (str): MD5 hash of the 1080p file that has been copied to the origin dir. 
        converted_path (str): Path of the 1080p file in the temp dir. 
        dest_path (str): Path of the 4k file in the temp dir. 
        og_path (str): Path fo the 4k file in the origin dir. 
        og_file_name (str): Name of the 4k file in the origin dir. 
    """
    if converted_file_copy_hash == converted_file_og_hash:
        logger.info(f"Converted file: {dest_path} in the temp directory and converted file in the original directory match")

        # Delete the converted copy in the temp directory
        os.remove(converted_path)
        logger.debug(f"Converted path: {converted_path} has been deleted.")

        # Delete the 4k copy in the temp directory
        os.remove(dest_path)
        logger.debug(f"4K copy path: {dest_path} has been deleted.")

        # Delete the 4k original in the origin directory
        os.remove(og_path)
        logger.debug(f"4K original: {og_path} has been deleted.")
        logger.info(f"Success in converting and removing files for {og_file_name}")
    else:
        file_error_logger.debug(f"There is an error with {converted_path}.")

def md5(file_name: str) -> str:
    """_summary_ Creates MD5 hash for the provided file path. Returns hexidigest str.

    Args:
        file_name (str): _description_

    Returns:
        str: _description_ returns hexdigest str.
    """
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
        bool: Returns True if video is 1920 x 1080, else returns False. 
    """
    #TODO: error handling

    try:
        probe = ffmpeg.probe(converted_path)
        width = probe['streams'][0]['width']
        height = probe['streams'][0]['height']
        if width == 1920:
            if height == 1080:
                logger.info(f"Return True - {converted_path} is 1920x1080.")
                return True
            else:
                logger.info(f"Return False - {converted_path} is not 1920x1080.")
                return False
        else:
            logger.info(f"Return False - {converted_path} is not 1920x1080.")
            return False

    except Exception as e:
        file_error_logger.debug(f"Error with: {converted_path}.  -> {e}")

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

        if is_feature_check_high_def_enabled() == True:
            if width >= 3840 and height >= 2160:
                logging.info(f"Return True - {original_path} is 3840 x 2160")
                return True
            else:
                logging.info(f"Return False - {original_path} is not 3840 x 2160")
                return False
        else:
            logging.info("Feature flag for checking high defintiion 4k video is off.")
        
    except KeyError as e:
        logging.info(f"Key error reported : {e}")

    except ffmpeg.Error as ex:
        logging.info("error with gathering video info %s", ex)

def get_original_file_paths(original_file_path: str) -> list:
    """Returns a list of each 4k file's path in the origin directory. 

    Args:
        origin_file_path (_str_): The directory path within your system for where the original 4k files reside.

    Returns:
        list: Returns a single list with paths of each 4k file in the directory for .mp4, .MP4, .mov, and .MOV files. 
    """
    for i in os.listdir(original_file_path):

        # This if statement is added to deal with AppleDouble Files on NAS. 
        if not i.startswith("._"):

        # Get the path of each file in the directory. 
            filename = os.path.basename(i)
            filepath = str(original_file_path) + '/' + i
            
            # Check the video file extension.  
            if filename.lower().endswith('.mp4') or filename.lower().endswith('.mov'):

            # Check the video resolution and verify it's a 4k file. 
                if check_high_def(filepath) == True:
                    logger.debug(f"{filepath} is verified to be in 4k.")
                    file_name_list.append(filename)
                    file_path_list.append(filepath)
        else:
            logger.debug(f"{i} appears to be an AppleDouble File is skipped.")
    logger.debug(f"Success in returning original file paths list.")            
    return file_path_list

def convert_to_1080p(hd_path_copy: str) -> str:
    """Converts a 4k file path to a 1080p file and returns the path for the 1080p file. 

    Args:
        path_copy (_str_): File path for the 4k copy in the temporary directory. 

    Returns:
        str: Returns the path of the 1080p copy in the temporary directory as a string. 
    """
    # Get the path string. 
    path_copy_base = str(os.path.basename(hd_path_copy).split('/')[-1])

    # Get the name from the original path string. 
    file_copy_name = (path_copy_base).split('.')[0]
    
    # Create the file extension from the original path string.
    file_ext = '.'+(path_copy_base).split('.')[1]

    # Create the path string for the file that's being copied. 
    path_copy_name = '/'.join(str(x) for x in (os.path.abspath(hd_path_copy).split('/')[:-1]))

    logger.debug(f"{path_copy_name} has successfully been created. Conversion process is starting.")

    # Run the conversion process. 
    conversion = subprocess.run(
        [
            'ffmpeg',
            '-i', 
            hd_path_copy,
            '-vf',
            'scale=1920:1080',
            '-c:a', 
            'copy',
            path_copy_name + '/' + file_copy_name + '_1080p' + file_ext,
            ]
            )
    
    return conversion




a = convert_videos_main("/Volumes/Videos/InProgressProjects/FSA Dollar Spend/Footage/1")
