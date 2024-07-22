# 4K to 1080p Scale Down

# To Do
- Add in feature showing how much space has been saved. 
- Add in a feature to show files that failed conversion. 
- 

## Purpose
Space is a luxury and 4k videos take up a ton of digital real estate. A lot of the space on NAS being taken up by older 4K footage that I still want to keep, but don't necessarily need in 4K anymore. With the numerous files and directories I have, I opted to write python program to go through and convert my files from 4K to 1080p using FFMPEG. 


## Summary
You'll provide a directory for the script to run through. It will identify all .mp4, .MP4, .mov, .MOV files in a resolution of 3840 x 2160 and convert those files to 1080p. 

## Process
1. Identify all of the 4k videos in the provided directory. 
2. Place the paths of those 4k files in a list. 
3. A for loop will run, doing the following:
   1. Create a 4k resolution copy in a secondary directory, not with the original 4k file.  
   2. Confirm, by the file size and video length, that the 4k original and 4k copy match. 
   3. Convert the 4k copy to 1080p and place in the secondary directory with "_1080p" appended to the file name, prior to the extension. 
   4. Confirm the conversion was successful by checking that the newly converted 1080p file has a frame size of 1920 x 1080.
   5. Copy the converted 1080p copy in the secondary directory to the original 4k file's directory. 
   6. Verify the 1080p copy was successfully copied to the original 4k files directory by again, checking the size and length of the 1080p copy in the original 4k directory matches that of the 1080p copy in the secondary directory. 
   7. Delete the 1080p copy in the secondary directory. 
   8. Delete the 4k copy in secondary directory. 
   9. Delete the original 4k file in the original directory. 
   10. Move onto the next path in the list. 
'''
