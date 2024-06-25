from header import *

def check_standard_def(converted_path) -> bool:
    """Checks the provided file path to verify the converted file is 1920 x 1080 resolution. 

    Args:
        converted_path (_str_): File path as a string for where the converted video file resides. 

    Returns:
        bool: _descri
    """
    probe = ffmpeg.probe(converted_path)
    width = probe['streams'][0]['width']
    height = probe['streams'][0]['height']
    if width == 1920:
        if height == 1080:
            print(f'Return True - {converted_path} is 1920x1080')
            return True
        else:
            print(f'Return False - {converted_path} is not 1920x1080')
            return False
    else:
        print(f'Return False - {converted_path} is not 1920x1080')
        return False