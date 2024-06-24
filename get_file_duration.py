from header import *


def get_length(input_video) -> float:
    result = subprocess.run(
        [
            'ffprobe', 
            '-v', 
            'error', 
            '-show_entries', 
            'format=duration', 
            '-of', 
            'default=noprint_wrappers=1:nokey=1', 
            input_video
            ], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT
            )
    return float(result.stdout)