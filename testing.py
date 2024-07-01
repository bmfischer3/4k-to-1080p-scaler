import unittest
import conversion
from dotenv import load_dotenv
import os
import sys

# Get values of the environment variables
original_file_path = os.getenv("ORIGINAL_FILE_PATH")
temp_file_path = os.getenv("TEMP_FILE_PATH")
feature_check_high_def = bool(os.getenv("FEATURE_CHECK_HIGH_DEF"))
feature_run_main = bool(os.getenv("FEATURE_RUN_MAIN"))
test_path_1_4k = os.getenv("TEST_PATH_1")
test_path_2_4k = os.getenv("TEST_PATH_2")
test_path_3_1080 = os.getenv("TEST_PATH_3")

test_path_4_4kA = os.getenv("TEST_PATH_4")
test_path_5_4kA = os.getenv("TEST_PATH_5")
test_path_6_4kA = os.getenv("TEST_PATH_6")

converted_path_4 = os.getenv("CONVERTED_PATH_4")
converted_path_5 = os.getenv("CONVERTED_PATH_5")
converted_path_6 = os.getenv("CONVERTED_PATH_6")

origin_file_directory = os.getenv("ORIGIN_FILE_DIRECTORY")


class TestConversion(unittest.TestCase):
    
    def test_hash(self):
        # Don't know what the hashes would be, so we wouldn't test?
        # vid_1 = conversion.md5(test_path_1_4k)
        # vid_2 = conversion.md5(test_path_2_4k)
        pass
    
    def test_standard_def(self):
        vid_1 = conversion.check_standard_def(test_path_1_4k)
        vid_2 = conversion.check_standard_def(test_path_2_4k)
        vid_3 = conversion.check_standard_def(test_path_3_1080)

        self.assertEqual(vid_1, False)
        self.assertEqual(vid_2, False)
        self.assertEqual(vid_3, True)

    def test_high_def(self):
        vid_1 = conversion.check_high_def(test_path_1_4k)
        vid_2 = conversion.check_high_def(test_path_2_4k)
        vid_3 = conversion.check_high_def(test_path_3_1080)

        self.assertEqual(vid_1, True)
        self.assertEqual(vid_2, True)
        self.assertEqual(vid_3, False)

    # def test_conversion(self):
    #     vid_1 = conversion.convert_to_1080p(test_path_4_4kA)
    #     vid_2 = conversion.convert_to_1080p(test_path_5_4kA)
    #     vid_3 = conversion.convert_to_1080p(test_path_6_4kA)

    #     self.assertEqual(vid_1, converted_path_4)
    #     self.assertEqual(vid_2, converted_path_5)
    #     self.assertEqual(vid_3, converted_path_6)

    def test_get_original_file_paths(self):
        # dir_A = origin_file_directory
        # self.assertEqual(dir_A, )
        pass





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

