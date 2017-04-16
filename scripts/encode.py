"""
This python script encodes all files that have the extension mkv in the current
working directory.

Sources:
    http://ffmpeg.org/trac/ffmpeg/wiki/x264EncodingGuide
"""
import os
import shutil
import subprocess

# ------------------------------------------------------------------------------
# CONFIGURABLE SETTINGS
# ------------------------------------------------------------------------------

# Quality of the encode, the lower the number the better.
CRF_VALUE = '21'

# h.264 profile.
PROFILE = 'high'

# Encoding speed:compression ratio.
PRESET = 'fast'

# Path to FFMPEG binary.
FFMPEG_PATH = 'G:\\ffmpeg\\bin\\ffmpeg.exe'

# Font dir.
FONT_DIR = 'G:\\ffmpeg\\bin\\fonts'

# Font config file.
FONTCONFIG_FILE = 'G:\\ffmpeg\\fonts.conf'

# ------------------------------------------------------------------------------
# encoding script
# ------------------------------------------------------------------------------


def rm(path):
    """Removes a file/directory if it exists."""
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)        
    

def process():
    cwd = os.getcwd()

    # get a list of files that have the extension mkv
    filelist = filter(lambda f: f.split('.')[-1] == 'mkv', os.listdir(cwd))
    filelist = sorted(filelist)

    # encode each file
    for file in filelist:
        encode(file)


def encode(file):
    name = ''.join(file.split('.')[:-1])
    subtitles = 'temp.ass'
    output = '{}.mp4'.format(name)

    try:
        # Base command to encoding a video.
        command = [
            FFMPEG_PATH, '-i', file,
            '-c:v', 'libx264',
            '-tune', 'animation',
            '-preset', PRESET,
            '-profile:v', PROFILE,
            '-crf', CRF_VALUE,
        ]

        cwd = os.getcwd()

        # Recreate FONT_DIR.
        rm(FONT_DIR)
        os.makedirs(FONT_DIR)
        os.chdir(FONT_DIR)

        # Dump attachments into FONT_DIR.
        subprocess.call([
            FFMPEG_PATH, '-dump_attachment:t', '',
            '-i', os.path.join(cwd, file)
        ])

        os.chdir(cwd)

        # extract ass subtitles and and subtitle into command
        subprocess.call([FFMPEG_PATH, '-i', file, subtitles])
        if os.path.getsize(subtitles) > 0:
            command += ['-vf', 'ass={}'.format(subtitles)]

        command += ['-c:a', 'copy']
        command += ['-threads', '4', output]
        subprocess.call(command) # encode the video!
    finally:
        # always cleanup even if there are errors
        rm(FONT_DIR)
        rm(subtitles)


if __name__ == "__main__":
    os.environ['FONTCONFIG_FILE'] = FONTCONFIG_FILE
    process()
