import unittest
import main
from dotenv import load_dotenv
import os
import sys

# Get values of the environment variables
original_file_path = os.getenv("ORIGINAL_FILE_PATH")
temp_file_path = os.getenv("TEMP_FILE_PATH")
feature_check_high_def = bool(os.getenv("FEATURE_CHECK_HIGH_DEF"))
feature_run_main = bool(os.getenv("FEATURE_RUN_MAIN"))

class LearningCase(unittest.TestCase):
    def test_starting_out(self):
        # make takes in expected file size
        expected_size = 1080

        main.main(expected_size)

        actual_file_size = main.get_file_size()

        self.assertEqual(expected_size, actual_file_size)




def main():
    unittest.main()

if __name__ == "__main__":
    main()



# TODO: Read up on this: https://docs.python.org/3/library/unittest.html 

