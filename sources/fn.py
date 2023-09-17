# -*- coding: utf-8 -*-
'''Ask functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import os, sys, moviepy, subprocess, webbrowser
from pytube import YouTube
import sources.txt as txt

def check_input_vars(separate, resolution):
    if separate == False and int(resolution[:-1]) > 720:
        print('\n!Correction.') 
        print(f'Resolution {resolution}px is too high for a video with one audio and video file')
        print('Video downloads changed to two files: an audio and a video file')
        separate = True 

    return separate, resolution


def check_for_modules():
    err, cmd = '', 'Installation command: python -m pip install '
    mod = lambda m: f'Please install <{m}> module which is currently not installed.\n'

    try: 
        import pytube
        assert pytube
    except ImportError: 
        err += mod('pytube')
        cmd += 'pytube '
    try: 
        import moviepy.editor
        assert moviepy.editor
    except ImportError: 
        err += mod('moviepy')
        cmd += 'moviepy '
    try: 
        import webbrowser
        assert webbrowser
    except ImportError: 
        err += mod('webbrowser')
        cmd += 'webbrowser '

    if err: 
        sys.stderr.write(f'{err}{cmd}\n')
        sys.exit(-1)

def remove(f):
    if os.path.exists(f):
        os.remove(f)

def rename(f1, f2):
    if os.path.exists(f1):
        if os.path.exists(f2):
            remove(f2)
        os.rename(f1, f2)

def get_youtube( yt, progressive="False", typ='video', mime_type="video/mp4",
                 audio_only=False, resolution=cfg.ask_default_resolution
                 ):
    '''Get a stream from Youtube'''

    # Get an audio stream
    if audio_only: 
        stream = yt.streams.filter( progressive=progressive, type=typ, mime_type=mime_type,
                                    only_audio=audio_only ).desc().first()        
        if not stream: 
            # Get any audio stream
            stream = yt.streams.filter(only_audio=audio_only).desc().first() 
    
    # Get a video stream
    else:
        stream = yt.streams.filter( progressive=progressive, type=typ, mime_type=mime_type,
                                    res=resolution ).desc().first()
        if not stream: 
            # Get other resolution streams
            for px in txt.lst_pixels:
                stream = yt.streams.filter(type=typ, res=px+'p').desc().first()
                if stream: 
                    break
            else:
                # Get a video whatever
                stream = yt.streams.first(type=typ)

    if stream: 
        return stream

    return False # No stream found

def get_audio_only_stream(yt):
    ''' Get an audio stream '''
    return get_youtube( yt, progressive='False', typ='audio', audio_only=True )

def get_video_only_stream(yt, resolution=cfg.ask_default_resolution):
    ''' Get a video only stream of a certain resolution.'''
    return get_youtube( yt, progressive='False', typ='video', mime_type='video/mp4', resolution=resolution )

def get_audio_and_video_stream(yt, resolution=cfg.ask_default_resolution):
    ''' Get a video and audio stream in one video of a certain resolution.'''
    return get_youtube( yt, progressive='True', typ='video', mime_type='video/mp4', resolution=resolution )

def process_dir( dir ):
    '''Make directory(s) for saving the file '''
    root = os.path.dirname( os.path.abspath(__file__) )
    mdir = os.path.join(root, dir)

    if not os.path.exists(mdir):
        os.makedirs( mdir )
        t = 'created'
    else:
        t = 'already exists'

    print(f'\nMap: {mdir}\n{t}')

    return mdir

def youtube(url):
    ok, yt, title, description = True, None, '', ''
    try: # Get meta info movie parameters
        yt = YouTube(url)
        # Does not work for audio, ok
        # if yt.check_availability():
        #     pass 
        # else:
        #     raise Exception('Video is not available')
            
    except Exception as e:
        print(f'Error in stream\nUrl: "{url}"\n{e}')
        ok = False
    else:
        # Print media info (if there)
        print('\nYouTube video found.')
        print(f'Url: "{url}"')

        if yt.title:
            title = txt.clean_spaces(yt.title)[:100] # Shortened a bit
            print(f'Title: {title}')
        else:
            print(f'No title found!')

        if yt.description:
            description = txt.clean_spaces(yt.description)[:500] # Shortened
            print('Description')
            print(description)
        else:
            print(f'No description found!')

        print(' ')
            
    return ok, yt, title, description

def process_video_only(yt, url, download_map, resolution):
    ok, path = True, ''

    try: # Process video
        print('Download video only')
        print(f'Resolution is: {resolution}')
        print(f'From: "{url}"')
        print(f'To: "{download_map}"\n')

        stream = get_video_only_stream(yt, resolution)
        if stream:
            path = stream.download(download_map)
        else:
            raise Exception('Video stream seems to be empthy')
        
    except Exception as e:
        print(f'Download error in video stream: {stream}\n{e}\n')
        ok = False

    else:
        print('Download video successful.')
        print(f'To: "{path}"\n')

    return ok, path

def process_video_and_audio(yt, url, download_map, resolution):
    ok, path = True, ''

    try: # Process video
        print(f'Download video and audio in one file')
        print(f'Resolution is: {resolution}')
        print(f'From: "{url}"')
        print(f'To: "{download_map}"\n')

        stream = get_audio_and_video_stream(yt, resolution)
        if stream:
            path = stream.download(download_map)
        else:
            raise Exception('Video stream seems to be empthy')
        
    except Exception as e:
        print(f'Download error in video stream:\n{stream}\n{e}\n')
        ok = False

    else:
        print('Download video successful.')
        print(f'To: "{path}"\n')

    return ok, path

def process_audio_only(yt, url, download_map):
    ok, path, stm = True, '', ''

    try: # Process audio
        print(f'Download audio only')
        print(f'From: "{url}"')
        print(f'To: "{download_map}"\n')

        stm = get_audio_only_stream( yt )
        if stm:
            path = stm.download(output_path=download_map)
        else:
            raise Exception('Audio stream seems to be empthy')

    except Exception as e:
        print(f'Error in audiostream: {stm}\n{e}\n')
        ok = False

    else:
        print(f'Download audio successful.')
        print(f'To: "{path}"\n')

    return ok, path


def audio_to_mp3(audio_path):
    ok, path = True, audio_path

    try: # Make mp3 file
        base, ext = os.path.splitext(audio_path)
        audio_mp3 = f'{base}.mp3'

        print(f'Convert clip to mp3 {audio_path}')
        clip = moviepy.editor.AudioFileClip(audio_path)
        clip.write_audiofile(audio_mp3)

    except Exception as e:
        print(f'Error in converting {audio_path}')
        print(f'To {audio_mp3} \n{e}')
        ok = False

    else:
        remove(audio_path) # Remove old audio file
        print('Audio mp3 created successful')
        path = audio_mp3

    return ok, path 


def merge_video_and_audio(video_path, audio_path):
    ok, path = True, ''

    print('Merge video and audio to one file.')
    print(f'Audio: "{audio_path}"')
    print(f'Video: "{video_path}"')
    print(f'To video: "{video_path}"\n')

    try: # Make video clip
        # Rename old file names for correct merging (anyway)
        base_video, ext_video = os.path.splitext(video_path)
        base_audio, ext_audio = os.path.splitext(audio_path)
        copy_video_path = f'{base_video}-video{ext_video}'
        copy_audio_path = f'{base_audio}-audio{ext_audio}'
        rename(video_path, copy_video_path)
        rename(audio_path, copy_audio_path)

        # Moviepy video and audio objects
        video_clip = moviepy.editor.VideoFileClip(copy_video_path) 
        audio_clip = moviepy.editor.AudioFileClip(copy_audio_path)

        # Merge video and audio into final clip
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(video_path)

    except Exception as e:
        print(f'Error in merging video and audiostream\n{e}\n')
        ok = False

    else:
        print(f'Merging video and audiostream successful\n')
        remove(copy_video_path) # Remove old video file
        remove(copy_audio_path) # Remove old audio file
        path = video_path # Done

    return ok, path

def exec_with_app(path):
    '''Function opens a file with an default application'''
    ok, err = True, ''

    # Linux
    if sys.platform.startswith('linux'):
        try:
            subprocess.call( ['xdg-open', path] )
        except Exception as e:
            err += f'{e}\n'
            try:
                os.system(f'start {path}')
            except Exception as e:
                err += f'{e}\n'
                ok = False

    # OS X
    elif sys.platform.startswith('darwin'): # ?
        try: 
            os.system( f'open "{path}"' )
        except Exception as e: 
            err += f'{e}\n'
            ok = False

    # Windows
    elif sys.platform in ['cygwin', 'win32']:
        try: # Should work on Windows
            os.startfile(path)
        except Exception as e:
            err += f'{e}\n'
            try:
                os.system( f'start "{path}"' )
            except Exception as e:
                err += f'{e}\n'
                ok = False

    # Possible fallback, use the webbrowser
    if not ok:
        try: webbrowser.open(path, new=2, autoraise=True)
        except Exception as e: 
            err += e
            ok = False

    if ok: 
        print('Open file with an app successful\n')
    else: 
        print(f'Error open file with an app.\n{err}\n')

    return ok