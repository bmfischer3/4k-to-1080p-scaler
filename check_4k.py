from header import *

def check_high_def(original_path) -> bool:
    """ Check the resolution of file and returns true if in 3840 x 2160

    Args:
        original_path (_str_): Path name to video file as a string. 

    Returns:
        bool: Returns true if the file is in a 4k resolution, 3840 x 2160
    """
    probe = ffmpeg.probe(original_path)

    # Get the height and width from the returned json data in ffmpeg.probe. 
    width = probe['streams'][0]['width']
    height = probe['streams'][0]['height']

    # check the width and height. 
    if width == 3840:
        if height == 2160:
            print(f'Return True - {original_path} is 3840 x 2160')
            return True
        else:
            print(f'Return False - {original_path} is not 3840 x 2160')
            return False
    else:
        print(f'Return False - {original_path} is not 3840 x 2160')
        return False