# 4K to 1080p Video Converter

## Table of Contents
- [4K to 1080p Video Converter](#4k-to-1080p-video-converter)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Business Problem](#business-problem)
  - [Methods](#methods)
  - [Tech Stack](#tech-stack)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Quick Glance at Results from Example Footage](#quick-glance-at-results-from-example-footage)
  - [Limitations](#limitations)
  - [Improvements](#improvements)
  - [Other Resources](#other-resources)
  - [Repository Structure](#repository-structure)
  - [Revision History](#revision-history)

## Overview
This project uses ffmpeg to convert 4k .mov and .mp4 files to 1080p. 


## Business Problem
Video that I shoot on my A7Siii is a 4k resolution with 100Mbps bitrate, which tends to produce large file sizes. Couple this with a Ninja V and the files are even larger when recorded in ProRes Raw. Storage space is not unlimited and there are many projects I have where I do not need to archive the 4k file. 

Significant disk space has been taken up by older 4K footage that I still want to keep, but don't necessarily need in 4K anymore. With the numerous files and directories I have, I opted to write python program to go through and convert my files from 4K to 1080p using ffmpeg rather than go through each file one by one in Final Cut or Premiere Pro. 


## Methods

The general process is as follows as below. Should an inssue occur at any point in the conversion process, the original 4k file will not have been moved or modified. 

1. Identify all of the 4k videos in the provided directory. 
2. Place the paths of those 4k files in a list. 
3. A for loop will run, doing the following:
   1. Create a 4k resolution copy in a secondary directory, not with the original 4k file. This is specified in as a .env variable.  
   2. Confirm, by md5 hash, that the 4k original and 4k copy match. 
   3. Convert the 4k copy to 1080p and place in the secondary directory with "_1080p" appended to the file name, prior to the extension. 
   4. Confirm the conversion was successful by checking that the newly converted 1080p file has a frame size of 1920 x 1080.
   5. Copy the converted 1080p copy in the secondary directory to the original 4k file's directory. 
   6. Verify the 1080p copy was successfully copied to the original 4k files directory by again, checking the md5 hash of the 1080p copy in the original 4k directory matches that of the 1080p copy in the secondary directory. 
   7. Delete the 1080p copy in the secondary directory. 
   8. Delete the 4k copy in secondary directory. 
   9. Delete the original 4k file in the original directory. 
   10. Move onto the next path in the list. 

## Tech Stack
Detail the technologies and libraries used in the project.

- **Programming Language**: Python
- **Libraries/Frameworks**:
  - `ffmpeg`- [ffmpeg](https://www.ffmpeg.org/about.html)


## Installation
Instructions for setting up the project on a local machine.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bmfischer3/4k-to-1080p-scaler.git
   cd repo
   ```

1. **Create and active a virtual environment:**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

1. **Install dependenceies:**
    ```bash
    pip install -r requirements.txt
   ```

1. **Set up environment variables:**
    ```bash
   ORIGINAL_FILE_PATH="<where the original 4k files live>"
   TEMP_FILE_PATH="<temporary path for where videos will be copied and converted to>"

   # Feature Flags

   FEATURE_CHECK_HIGH_DEF_ENABLED="True"
   GET_FINISHED_FILE_SIZE_ENABLED="True"
   LOGGING_ENABLED="True"

   # Testing .env variables

   1080P_CONVERT_TEST_PATH=""
   1080P_CONVERT_TEST_OUTPUT_PATH=""
   MD5_HASH_TEST_PATH=""
   CHECK_HIGH_DEF_TEST_PATH=""
   CHECK_ORIGINAL_PATH_TEST_PATH=""
   CHECK_STANDARD_DEF_TEST_PATH=""
   CHECK_FULL_CONVERSION_PATH=""

   ```

## Usage
Instructions for how to use the project.

1. **Step 1:**
   - details on step 1
    ```bash


## Quick Glance at Results from Example Footage
The below shows results from a test conversion using free stock footage. 

| **Example File Name**            | **Original 4k Size** | **Post Conversion Size** | **% Reduction** |
|----------------------------------|----------------------|--------------------------|-----------------|
| children_playing_in_fountain.mp4 |        79.2 MB       |          50.4 MB         |       36%       |
| ducks_on_water.mp4               |        97.4 MB       |          88.3 MB         |        9%       |
| people_hiking.mp4                |        49.4 MB       |          10.4 MB         |       79%       |
| woman_posing_for_camera.mp4      |        59.8 MB       |          7.8 MB          |       87%       |





## Limitations
- **File types**: Only files that are in a .mp4 and .mov file type can be converted. 
- **Frame Orientation**: This program can only convert 4k videos in landscape orientation. 4K files in portrait orientation cannot yet be converted. 
- **Windows**: This program was developed on macOS and has not been tested on windows. 
- **Metadata**: At this time, it does not appear the program maintains metadata on each file. 

## Improvements
- **Thread Limitation**: By default, ffmpeg will occupy 90%+ of CPU use, this can freeze other applications. Thread limitations would allow other programs to run while conversions are occurring. 
- **Error handling & Logging**: Additional error handling and logging details need to be added for clarity. 
- **Gather subdirectories**: Instead of supplying a single directory, a method to gather all subdirectories would be helpful. 
- **Ignore specific files**: For files within a directory that match a certain pattern, ignoring those files could prove useful. 
- **Time estimate**: Understand how long it will take the converter to finish processing the task at hand. 
- **GPU Acceleration**: For systems with a dedicated GPU, ffmpeg supports some level of GPU acceleration that wasn't explored with this project. 


## Other Resources
- **ffmpeg**[https://www.ffmpeg.org/about.html]


## Repository Structure
project-root/
├── conversion.py
├── testing.py
├── requirements.txt
├── README.md
└── .gitignore


## Revision History

This section documents the history of major changes made to the repository.

| Date       | Version | Author       | Description                                           |
|------------|---------|--------------|-------------------------------------------------------|
| 2024-07-22 | 1.0.0   | B. Fischer   | Cleaned up for release and publication.               |
| YYYY-MM-DD | X.X.X   | Your Name    | Description of the changes made.                      |
| YYYY-MM-DD | X.X.X   | Your Name    | Description of the changes made.                      |

