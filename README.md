# VA-Converter
A program for batch "merging" video and audio files.<br>

**It was made primarily for personal use**, but you never know who might find such a "crutch" useful.

The default is to use VLC, but other tools can potentially be used by specifying a different command template.<br>
Optionally, it can use [`tqdm`](https://pypi.org/project/tqdm/) to display brief information.

## Usage
```
usage: va-converter.exe [-h] [-od OUTPUT_DIR] [-vt VIDEO_TYPE] [-at AUDIO_TYPE]
                        [-ot OUTPUT_TYPE] [-vlc VLC] [-cmd-tl COMMAND_TEMPLATE] [--debug]
                        VIDEO_DIR AUDIO_DIR

A program for batch "merging" video and audio files. Version: 1.0

positional arguments:
  VIDEO_DIR             Directory of input video files.
  AUDIO_DIR             Directory of input audio files.

options:
  -h, --help            show this help message and exit
  -od OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory. (default: .\result)
  -vt VIDEO_TYPE, --video-type VIDEO_TYPE
                        Type of input video files. (default: .mkv)
  -at AUDIO_TYPE, --audio-type AUDIO_TYPE
                        Type of input audio files. (default: .mka)
  -ot OUTPUT_TYPE, --output-type OUTPUT_TYPE
                        Type of output files. (default: .mp4)
  -vlc VLC, --vlc VLC   Path to vlc player. (default: C:\Program
                        Files\VideoLAN\VLC\vlc.exe)
  -cmd-tl COMMAND_TEMPLATE, --command-template COMMAND_TEMPLATE
                        Command template for processing. (default: cmd /C ""{vlc}" -I
                        dummy "{video_file}" ":input-slave={audio_file}"
                        ":sout=#transcode{{}}:std{{dst=\"{output_file}\",access=file}}"
                        vlc://quit")
  --debug
```
