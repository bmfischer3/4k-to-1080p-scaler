import unittest
import conversion
from dotenv import load_dotenv
import os
import sys

# Get values of the environment variables

origin_file_paths = os.getenv("CHECK_ORIGINAL_PATH_TEST_PATH")
check_high_def_paths = os.getenv("CHECK_HIGH_DEF_TEST_PATH")
convert_to_1080_paths = os.getenv("1080P_CONVERT_TEST_PATH")
convert_to_1080_paths_output = os.getenv("1080P_CONVERT_TEST_OUTPUT_PATH")
md5_hashing_paths = os.getenv("MD5_HASH_TEST_PATH")
check_standard_def_paths = os.getenv("CHECK_STANDARD_DEF_TEST_PATH")
full_conversion_paths = os.getenv("CHECK_FULL_CONVERSION_PATH")


class TestConversion(unittest.TestCase):
    def test_check_get_original_file_paths(self):
        # Expected to return a list of paths for 4k files ending in .mp4 or .mov
        test_dir = origin_file_paths

        test_result = conversion.get_original_file_paths(test_dir)

        expected_result = [
                "/Users/brianfischer/Documents/4 - Data Storage/4k to 1080p Scale Down/testing/1_get_original_file_paths/file_1.MP4",
                "/Users/brianfischer/Documents/4 - Data Storage/4k to 1080p Scale Down/testing/1_get_original_file_paths/file_3.mP4",
                "/Users/brianfischer/Documents/4 - Data Storage/4k to 1080p Scale Down/testing/1_get_original_file_paths/file_4.mp4"
        ]

        # Clean the results by lowercasing everything and sorting the order. 

        expected_result_cleaned = []
        for i in expected_result:
            x = i.lower()
            expected_result_cleaned.append(x)


        test_result_cleaned = []
        for n in test_result:
            y = n.lower()
            test_result_cleaned.append(y)

        self.assertListEqual(sorted(test_result_cleaned), sorted(expected_result_cleaned))



    def test_check_high_def(self):
        
        path_list = []

        # Cannot use conversion.get_original_file_paths method because that will only append if those paths are in 4k, thus rendering everything True. 
        for i in os.listdir(check_high_def_paths):
            filepath = str(check_high_def_paths) + '/' + i
            path_list.append(filepath)
        path_list = sorted(path_list)

        # Create a list of bool values to evaluate. 
        status = []
        for i in path_list:
            print(i)
            n = conversion.check_high_def(i)
            status.append(n)
            print(n)

        self.assertEqual(status[0], True)
        self.assertEqual(status[1], False)
        self.assertEqual(status[2], True)
        self.assertEqual(status[3], True)


    # def test_check_convert_to_1080p(self):

    #     # Verify 4K files exist in the directory you're testing and match the below list. 
        
    #     # Get a list of the paths for 4k files

    #     expected_1080p_converted_paths_list = sorted([
    #         "/Users/brianfischer/Documents/4 - Data Storage/4k to 1080p Scale Down/testing/1_get_original_file_paths/converted/file_1_1080p.MP4",
    #         "/Users/brianfischer/Documents/4 - Data Storage/4k to 1080p Scale Down/testing/1_get_original_file_paths/converted/file_3_1080p.mP4",
    #         "/Users/brianfischer/Documents/4 - Data Storage/4k to 1080p Scale Down/testing/1_get_original_file_paths/converted/file_4_1080p.mp4"
    #     ])

    #     converted_paths_list = []

    #     for i in os.listdir(convert_to_1080_paths):
    #         if not i.startswith("._"):
    #             print(i)
    #             conversion.convert_to_1080p(i)
    #             print(f"converted {i}")
        
    #     for i in os.listdir(convert_to_1080_paths_output):
    #         filepath = str(convert_to_1080_paths_output) + '/' + i
    #         converted_paths_list.append(filepath)
    #         print(filepath)
        
    #     converted_paths_list = sorted(converted_paths_list)

    #     self.assertListEqual(expected_1080p_converted_paths_list, converted_paths_list)
            

        # Feed that list ot the 1080p conversion method. 
        # Check that it returns a string with teh 1080p files and teh 1080p name tagged on teh end. 


    def test_md5_hash(self):
        pass

    
    def test_check_standard_def(self):
        
        path_list = []

        # Cannot use conversion.get_original_file_paths method because that will only append if those paths are in 4k, thus rendering everything True. 
        for i in os.listdir(check_standard_def_paths):
            filepath = str(check_standard_def_paths) + '/' + i
            path_list.append(filepath)
        path_list = sorted(path_list)

        # Create a list of bool values to evaluate. 
        status = []
        for i in path_list:
            print(i)
            n = conversion.check_standard_def(i)
            status.append(n)
            print(n)

        self.assertEqual(status[0], False)
        self.assertEqual(status[1], True)
        self.assertEqual(status[2], False)
        self.assertEqual(status[3], False)

    # def test_check_full_conversion(self):
    #     vid_1 = conversion.convert_to_1080p(test_path_4_4kA)
    #     vid_2 = conversion.convert_to_1080p(test_path_5_4kA)
    #     vid_3 = conversion.convert_to_1080p(test_path_6_4kA)

    #     self.assertEqual(vid_1, converted_path_4)
    #     self.assertEqual(vid_2, converted_path_5)
    #     self.assertEqual(vid_3, converted_path_6)






    # def test_convert(self):

    #     # Set the expected file size. Ensure name matches the file name. 
    #     Christmas2021 = 117876406
    #     # Christmas2024 = 844938199
    #     Konro_Grill = 154139406
    #     Speaker_Design = 46287404

    #     test_list = []
    #     # a = main()

    #     # Get the actual size of the converted files that were placed back in the original directory. 

    #     for video_path in a:

    #         # Get the name of the video. Extension not needed. 
    #         completed_video_name = os.path.basename(video_path).split('/')[-1]

    #         # Get the size of the video in bytes. 
    #         video_path_size = os.stat(video_path).st_size

    #         # Create a list
    #         video_name_size_dict = {completed_video_name : video_path_size}

    #         # Append the list to a list. 

    #         test_list.append(video_name_size_dict)

    #     self.assertEqual(Christmas2021, test_list['Christmas2021'])
    #     self.assertEqual(Konro_Grill, test_list['Konro_Grill'])
    #     self.assertEqual(Speaker_Design, test_list['Speaker_Design'])



        # self.assertEqual(expected_size, actual_file_size)

def main():
    unittest.main()

if __name__ == "__main__":
    unittest.main()



# TODO: Read up on this: https://docs.python.org/3/library/unittest.html 

