
from check_standard_def import check_standard_def
from get_4k_file_paths import get_original_file_paths
from get_file_duration import get_length
from header import *

'''

Steps to Success

1. Identify all of the 4k videos in a directory. DONE
2. Place those file paths in a list. DONE
3. 1 by 1, create a secondary copy in a different location in Folder A. DONE
4. Confirm the secondary copy matches the original. DONE
----- check video file size and video length. DONE
5. Convert the secondary copy from 4K to 1080p and place in Folder A with "_1080p" appended to the end of the filename. DONE
6. Confirm the conversion was successful by checking that the newly outputed file has a frame size of 1920 x 1080 DONE
7. Copy the converted copy to the original file's location. 
8. Verify the converted copy was successfully copied to the origin. 
9. Delete the 1080p copy in Folder A. 
10. Delete the 4k copy in Folder A. 
11. Delete the 4k original in the origin. 
12. Print (Success)
13. Move on to the next file path in the list. 


'''

def convert_to_1080p(path_copy):
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


def main(file_path_list):

    # Create the path for the destination file
    dest_folder = "/Users/brianfischer/Documents/4 - Data Storage/4k to 1080p Scale Down/Folder1/TestC"

    for file in file_name_list:
        dest_path = dest_folder + "/" + file
        dest_filepath_list.append(dest_path)

    # Zip the lists

    combined_list_zipped = zip(file_path_list,dest_filepath_list)

    for og_path, dest_path in combined_list_zipped:
        # Create a copy of the original file in the temporary directory. 
        shutil.copy2(og_path, dest_path)

        # Get the size of each file in bytes and check the original and new copy match. 
        original_file_size = os.stat(og_path)
        copied_file_size = os.stat(dest_path)

        if original_file_size.st_size == copied_file_size.st_size:
            if get_length(og_path) == get_length(dest_path):
                print("original file and new file are the same size and duration")
                print(f"{original_file_size.st_size} is equal to {copied_file_size.st_size} in size. Duration checks out.")
        
                # Start converting the copied file. 
                convert_to_1080p(dest_path)

                og_file_name = (os.path.basename(og_path).split('/')[-1]).split('.')[0]
                file_ext = '.'+(os.path.basename(og_path).split('/')[-1]).split('.')[1]
                converted_path = '/'.join(str(x) for x in (os.path.abspath(dest_path)).split('/')[:-1]) + '/' + og_file_name + '_1080p' + file_ext

                if check_standard_def(converted_path) == True:
                    shutil.copy2(converted_path, og_path)
        
        else:
            print(f"Files are not the same size. {original_file_size} does not equal {copied_file_size} or the durations do not match. {og_path} and {dest_path} are the issues.")



a = main(origin_file_path)