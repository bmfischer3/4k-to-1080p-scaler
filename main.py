
from check_standard_def import check_standard_def
from convert_to_1080p import convert_to_1080p
from get_4k_file_paths import get_original_file_paths
from get_file_duration import get_length
from header import *


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

                # The below is the 1080p path where the 1080p file will go into the original 4k file's directory. 
                og_directory_1080_path = '/'.join(str(x) for x in (os.path.abspath(og_path)).split('/')[:-1]) + '/' + og_file_name + '_1080p' + file_ext


                # Verify the converted file is in 1080p. 
                if check_standard_def(converted_path) == True:

                    # Copy the converted 1080p file to the original 4k file's directory. 
                    shutil.copy2(converted_path, og_directory_1080_path)

                    # Verify the converted file was correctly copied to the original 4k file's directory. 
                    # Get the file size of the converted files in the copy and og path. 
                    converted_file_size_copy_path = os.stat(converted_path)
                    converted_file_size_og_path = os.stat(og_directory_1080_path)

                    if converted_file_size_og_path.st_size == converted_file_size_copy_path.st_size:
                        if get_length(converted_path) == get_length(og_directory_1080_path):
                            print("Converted file in the temp directory and converted file in the original directory match")

                            # Delete the converted copy in the temp directory
                            os.remove(converted_path)

                            # Delete the 4k copy in the temp directory
                            os.remove(dest_path)

                            # Delete the 4k original in the origin directory
                            os.remove(og_path)

                            print(f"Success in converting and removing files for {og_file_name}.")

                        else:
                            print("Converted files do not match. There was an error.")
                    else:
                        print("Converted files do not match. There was an error.")
        else:
            print(f"Files are not the same size. {original_file_size} does not equal {copied_file_size} or the durations do not match. {og_path} and {dest_path} are the issues.")



a = get_original_file_paths(origin_file_path)

b = main(a)