from header import *

def check_high_def(original_path) -> bool:
    probe = ffmpeg.probe(original_path)
    width = probe['streams'][0]['width']
    height = probe['streams'][0]['height']
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