from header import *

'''

Steps to Success

1. Identify all of the 4k videos in a directory. 
2. Place those file paths in a list. 
3. 1 by 1, create a secondary copy in a different location in Folder A. 
4. Confirm the secondary copy matches the original. 
5. Convert the secondary copy from 4K to 1080p and place in Folder A with "_1080p" appended to the end of the filename. 
6. Confirm the conversion was successful. 
7. Copy the converted copy to the original file's location. 
8. Verify the converted copy was successfully copied to the origin. 
9. Delete the 1080p copy in Folder A. 
10. Delete the 4k copy in Folder A. 
11. Delete the 4k original in the origin. 
12. Print (Success)
13. Move on to the next file path in the list. 


'''

file_name_list = []
file_path_list = []
dest_filepath_list = []

def get_4k_file_paths(origin_file_path):

    for i in os.listdir(origin_file_path):
        filename = os.path.basename(i)
        filepath = origin_file_path + i
        if filename.endswith(".mp4") or filename.endswith(".MP4") or filename.endswith(".MOV") or filename.endswith(".mov"):
            file_name_list.append(filename)
            file_path_list.append(filepath)
    # print(file_path_list)
    return file_path_list

def create_backup_copy(file_path_list):

    # Create the path for the destination file
    dest_folder = "/Users/brianfischer/Documents/4 - Data Storage/4k to 1080p Scale Down/Folder1/TestC"

    for file in file_name_list:
        dest_path = dest_folder + "/" + file
        dest_filepath_list.append(dest_path)

    for file in file_path_list:
        for dest_path in dest_filepath_list:
            shutil.copy2(file, dest_path)



def convert_4k_video()


a = get_4k_file_paths(origin_file_path)

b = create_backup_copy(a)