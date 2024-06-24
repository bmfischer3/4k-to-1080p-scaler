from header import *

def check_standard_def(converted_path) -> bool:
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