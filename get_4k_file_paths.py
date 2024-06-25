from check_4k import check_high_def
from header import *

def get_original_file_paths(origin_file_path) -> list:
    """_summary_

    Args:
        origin_file_path (_str_): The directory path within your system for where the original 4k files reside.

    Returns:
        list: Returns a single list with paths of each 4k file in the directory for .mp4, .MP4, .mov, and .MOV files. 
    """
    for i in os.listdir(origin_file_path):

        # Get the path of each file in the directory. 
        filename = os.path.basename(i)
        filepath = origin_file_path + i
        
        # Check the video file extension.  

        if filename.endswith(".mp4") or filename.endswith(".MP4") or filename.endswith(".MOV") or filename.endswith(".mov"):

        # Check the video resoloution and verify it's a 4k file. 

            if check_high_def(filepath) == True:
                file_name_list.append(filename)
                file_path_list.append(filepath)
                
    return file_path_list