# -*- coding: utf-8 -*-
'''Ask functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import os, sys, moviepy, subprocess, webbrowser
from pytube import YouTube
import sources.txt as txt

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

def get_stream_audio_only(yt):
    ''' Get an audio stream '''
    stm = yt.streams.filter( progressive="False", mime_type='audio/mp4', 
                             type='audio', only_audio=True ).desc().first()
    if stm: 
        return stm

    stm = yt.streams.filter(only_audio=True).desc().first() # Whatever
    return stm


def get_stream_video_only(yt, resolution):
    ''' Get a video stream of a certain resolution.'''
    # Get correct resolution
    stm = yt.streams.filter( progressive="False", mime_type="video/mp4", 
                             type="video", res=resolution ).desc().first()
    if stm: 
        return stm

    # Still nothing ? Get other resolution streams
    for pix in txt.lst_pixels:
        stm = yt.streams.filter(type="video", res=pix+'p').desc().first()
        if stm: 
            return stm

    # Get whatever
    stm = yt.streams.first(type="video")
    if stm: 
        return stm

    # Error
    print('Error', str(yt.streams))
 
    return False # ok give up

def get_clip_audio_and_video(yt, resolution):
    stm = yt.streams.filter( progressive="True", mime_type="video/mp4", 
                             res=resolution ).desc().first()
    if stm: 
        return stm
    
    # Still nothing ? Get other resolution streams
    for pix in txt.lst_pixels:
        stm = yt.streams.filter(ime_type="video/mp4", res=pix+'p').desc().first()
        if stm: 
            return stm

    # Get whatever
    stm = yt.streams.first()
    if stm: 
        return stm

    # Error
    print('Error', str(yt.streams))


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
        print('Check clip success.')
        print(f'Url: "{url}"')
        if yt.title:
            title = txt.clean_spaces(yt.title)[:100] # Shortened a bit
            print(f'Title: {title}')
        else:
            print(f'No clip title found!')

        if yt.description:
            description = txt.clean_spaces(yt.description)[:500] # Shortened
            print('Description')
            print(description)
        else:
            print(f'No clip description found!')

        print(' ')
            
    return ok, yt, title, description


def process_video(yt, url, download_map, video_res):
    ok, path = True, ''

    try: # Process video
        print(f'Download video from: {url}.')
        print(f'To directory: {download_map}\n')

        stream = get_stream_video_only(yt, video_res)
        if stream:
            path = stream.download(download_map)
        else:
            raise Exception('Video stream seems to be empthy')
        
    except Exception as e:
        print(f'Download error in video stream: {stream}\n{e}\n')
        ok = False

    else:
        print('Download video successful.')
        print(f'To: {path}\n')

    return ok, path


def process_audio(yt, url, download_map):
    ok, path, stm = True, '', ''

    try: # Process audio
        print(f'Download audio from: {url}')
        print(f'To directory: {download_map}\n')

        stm = get_stream_audio_only( yt )
        if stm:
            path = stm.download(output_path=download_map)
        else:
            raise Exception('Audio stream seems to be empthy')

    except Exception as e:
        print(f'Error in audiostream: {stm}\n{e}\n')
        ok = False
    else:
        print(f'Download audio successful.')
        print(f'To: {path}\n')

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

    print('Make videoclip: merge video and audio.')
    print(f'From audio: {audio_path}')
    print(f'From video: {video_path}')
    print(f'To audio and video: {video_path}\n')

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
        print(f'Error in merging video and audiostream\n{e}')
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
        print('Open file with an app successful')
    else: 
        print(f'Error open file with an app.\n{err}')

    return ok