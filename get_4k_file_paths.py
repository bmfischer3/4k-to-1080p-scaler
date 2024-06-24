from check_4k import check_high_def
from header import *

def get_original_file_paths(origin_file_path) -> list:
    for i in os.listdir(origin_file_path):
        filename = os.path.basename(i)
        filepath = origin_file_path + i
        
        # Check the video file extension.  

        if filename.endswith(".mp4") or filename.endswith(".MP4") or filename.endswith(".MOV") or filename.endswith(".mov"):
        # Check the video resoloution
            if check_high_def(filepath) == True:
                file_name_list.append(filename)
                file_path_list.append(filepath)
                
    return file_path_list