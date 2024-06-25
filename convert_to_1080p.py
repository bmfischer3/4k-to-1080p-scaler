from header import *

def convert_to_1080p(path_copy) -> str:
    """_summary_

    Args:
        path_copy (_str_): File path for the 4k copy in the temporary directory. 

    Returns:
        str: Returns the path of the 1080p copy in the temporary directory as a string. 
    """
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