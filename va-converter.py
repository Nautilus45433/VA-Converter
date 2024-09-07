import argparse
import glob
import logging
import os
import sys

try:
    import tqdm
except:
    tqdm = None


def arg_parse():
    parser = argparse.ArgumentParser(description='A program for batch "merging" video and audio files. Version: 1.0',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('VIDEO_DIR', type=str, help='Directory of input video files.')
    parser.add_argument('AUDIO_DIR', type=str, help='Directory of input audio files.')
    parser.add_argument('-od', '--output-dir', type=str, help='Output directory.', default='.\\result')
    parser.add_argument('-vt', '--video-type', type=str, help='Type of input video files.', default='.mkv')
    parser.add_argument('-at', '--audio-type', type=str, help='Type of input audio files.', default='.mka')
    parser.add_argument('-ot', '--output-type', type=str, help='Type of output files.', default='.mp4')
    parser.add_argument('-vlc', '--vlc', type=str, help='Path to vlc player.', default='C:\\Program Files\\VideoLAN\\VLC\\vlc.exe')
    parser.add_argument('-cmd-tl', '--command-template', type=str, help='Command template for processing.',
                        default='cmd /C ""{vlc}" -I dummy "{video_file}" ":input-slave={audio_file}" ":sout=#transcode{{}}:std{{dst=\\"{output_file}\\",access=file}}" vlc://quit"')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    try:
        if not os.path.isdir(args.VIDEO_DIR):
            raise ValueError('VIDEO_DIR')
        if not os.path.isdir(args.AUDIO_DIR):
            raise ValueError('AUDIO_DIR')
        if not os.path.isfile(args.vlc):
            raise ValueError('VLC')
    except:
        logging.exception('')
        logging.critical('Shutdown.')
        sys.exit()

    return parser, args


def init_logger(level):
    log_format = logging.Formatter('[%(asctime)+23s] [%(levelname)+4s]: %(message)s')
    root_logger = logging.getLogger(None)
    root_logger.setLevel(level)
    if len(root_logger.handlers):
        root_logger.removeHandler(root_logger.handlers[0])
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)


def main():
    init_logger(logging.INFO)
    parser, args = arg_parse()
    log_level = logging.DEBUG if args.debug else logging.INFO
    init_logger(log_level)

    info = list()
    for a in parser._actions[1:]:
        desc = (a.help[:-1] if a.help is not None else a.dest) + ' '
        info.append(f'{desc:.<33} : {repr(args.__dict__[a.dest])}')
    video_files = glob.glob(os.path.join(glob.escape(args.VIDEO_DIR), f'*{args.video_type}'))
    file_count = len(video_files)
    info.append(f'{"File pairs to process ":.<33} : {file_count}')
    logging.info('Info:\n    ' + '\n    '.join(info))

    input('Press ENTER to continue . . o.')
    
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
        logging.info(f'A directory for output files has been created: {repr(args.output_dir)}.')

    logging.info('Start processing files.')

    if not args.debug and tqdm is not None:
        video_files = tqdm.tqdm(video_files)

    for i, video_file in enumerate(video_files):
        i += 1
        if not os.path.isfile(video_file):
            logging.warning(f'[{i:0>2} / {file_count:0>2}] Video file {repr(video_file)} not found. Skip.')
            continue
        video_file_basename = os.path.splitext(os.path.basename(video_file))[0]
        audio_file = os.path.join(args.AUDIO_DIR, f'{video_file_basename}{args.audio_type}')
        if not os.path.isfile(audio_file):
            logging.warning(f'[{i:0>2} / {file_count:0>2}] Audio file {repr(video_file)} not found. Skip.')
            continue
        output_video_file = os.path.join(args.output_dir, f'{video_file_basename}{args.output_type}')
        
        if not args.debug and tqdm is not None:
            video_files.set_description(f'[{output_video_file}]')

        cmd = args.command_template.format(
            vlc=args.vlc,
            video_file=video_file,
            audio_file=audio_file,
            output_file=output_video_file)
        
        if args.debug or tqdm is None:
            logging.log(log_level, f'[{i:0>2} / {file_count:0>2}] Start of processing:\n    Video .. : {video_file}\n    Audio .. : {audio_file}\n    Output . : {output_video_file}')
        
        logging.debug(f'[{i:0>2} / {file_count:0>2}] Command:\n{cmd}')
        os.system(cmd)
        
        if args.debug or tqdm is None:
            logging.log(log_level, f'[{i:0>2} / {file_count:0>2}] End of processing.')

    logging.info('Finish processing files.')
    logging.info('Shutdown.')


if __name__ == '__main__':
    main()
