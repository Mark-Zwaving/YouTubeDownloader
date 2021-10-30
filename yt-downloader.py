# -*- coding: utf-8 -*-
'''Program downloads an video/mp3 from youtube based on an id or a complete url'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

#  Use: python version >= 3.7
#  Install modules: python -m pip install pytube moviepy webbrowser
#  If url via share does not work, check youtube url in browser
#  Install ffmpeg

import os, sys, re, webbrowser, subprocess

# Check for modules
err, cmd = '', 'Installation command: python -m pip install '
mod = lambda m: f'Please install <{m}> module which is currently not installed.\n'
try: import pytube; assert pytube
except ImportError: err += mod('pytube'); cmd += 'pytube '
try: import moviepy.editor; assert moviepy.editor
except ImportError: err += mod('moviepy'); cmd += 'moviepy '
if err: sys.stderr.write(err + cmd + '\n'); sys.exit(-1)

# Available resolutions
pixels    =  [ '2160p', '1440p', '1080p', '720p', '360p', '240p', '144p' ]
answ_yes  =  [ 'y', 'yes', 'ok', 'oke', 'j', 'yee' ]
answ_no   =  [ 'n', 'no', 'nee', 'nope', 'nada' ]
answ_quit =  [ 'q', 'stop', 'done', 'quit' ]
base_url  =  'https://www.youtube.com/watch?v='
ask       =  lambda t : input(f'\n{t}\n ? ').strip()

def clean_spaces(s):
    '''Remove unnecessary (double) whitespaces'''
    s = re.sub('\n\n+', '\n', s)
    s = re.sub('\s\s+', ' ', s)
    return s

def newname(f):
    l = f.split('.')
    return f'{l[0]}__.{l[1]}'

def oldname(f):
    l = f.split('.')
    return f'{l[0][:-2]}.{l[1]}'

def remove(f):
    if os.path.exists(f):
        os.remove(f)

def rename(f1, f2):
    if os.path.exists(f1):
        if os.path.exists(f2):
            remove(f2)
        os.rename(f1, f2)

def get_audio(yt):
    ''' Get an audio stream '''
    stm = yt.streams.filter( mime_type='audio/mp4', type='audio',
                             only_audio=True ).desc().first()
    if stm: return stm

    stm = yt.streams.filter(only_audio=True).desc().first()
    return stm

def get_video(yt, res):
    ''' Get a video stream of a certain resolution.'''
    # Get correct resolution
    stm = yt.streams.filter(mime_type='video/mp4', res=res).desc().first()
    if stm: return stm, res

    stm = yt.streams.filter(res=res).desc().first()
    if stm: return stm, res

    # Still nothing ? Get other resolution streams
    for pix in pixels:
        stm = yt.streams.filter(res=pix).desc().first()
        if stm: return stm, pix

    # Get whatever
    stm = yt.streams.first()
    if stm: return stm, res

    # Error
    print('Error', str(yt.streams), '\nRes:', res)
    return False, 0

def open_with_app(txt, path):
    '''Ask for opening a downloaded media file'''
    t  = f'{txt} ?\n{path}\n'
    t += "Type 'y' for yes.\nPress <enter> for no. \n"
    t += "Press 'q' to quit"
    answ = ask(t)

    if answ in answ_yes:
        ok, err = False, ''

        # Linux
        if sys.platform.startswith('linux'):
            try:
                subprocess.call( ["xdg-open", path] )
            except Exception as e:
                err += e+'\n'
                try:
                    os.system(f'start {path}')
                except Exception as e:
                    err += e+'\n'
                else:
                    ok = True
            else:
                ok = True

        # OS X
        elif sys.platform == "darwin":
            try:
                os.system( f'open "{path}"' )
            except Exception as e:
                err += e+'\n'
            else:
                ok = True

        # Windows...
        elif sys.platform in ['cygwin', 'win32']:
            try: # should work on Windows
                os.startfile(path)
            except Exception as e:
                err += e+'\n'
                try:
                    os.system( f'start "{path}"' )
                except Exception as e:
                    err += e+'\n'
                else:
                    ok = True
            else:
                ok = True

        # Possible fallback, use the webbrowser
        if not ok:
            try:
                webbrowser.open_new_tab(path)
            except Exception as e:
                err += e+'\n'
            else:
                ok = True

        t = f'Open {path} '
        if not ok:
            t += 'failed\n'
            t += err
            print(t)
        else:
            t += 'succesfull'
            # pass

        return 1

    elif answ in answ_quit:
        return answ_quit[0]

def process_dir( dir ):
    '''Make directory(s) for saving the file '''
    root = os.path.dirname( os.path.abspath(__file__) )
    mdir = os.path.join(root, dir)

    if not os.path.exists(mdir):
        os.makedirs( mdir )
        t = 'created'
    else:
        t = 'already exists'
    print(f'\nMap: {mdir} {t}')

    return mdir

# View
def ask_yt_url():
    t  = 'Give/paste a complete youtube URL.\n'
    t += 'Or put only the ID-part in the url /watch?v=<ID>?\n'
    t += "Press 'q' to quit"
    answ = ask( t )
    if answ in answ_quit:
        return answ_quit[0]
    else:
        return answ if 'https://' in answ else f'{base_url}{answ}'

def ask_audio_only():
    t  = 'Audio only ?\n'
    t += "Type 'y' for yes.\nPress <enter> for no. \n"
    t += "Press 'q' to quit"
    answ = ask( t )
    if answ in answ_quit:
        return answ_quit[0]
    elif answ in answ_yes:
        return True
    else:
        return False

def ask_audio_to_mp3():
    t  = f'Do you want to change the media file to a mp3 file ? \n'
    t += "Type 'y' for yes.\nPress <enter> for no. \n"
    t += "Press 'q' to quit"
    answ = ask(t)
    if answ in answ_quit:
        return answ_quit[0]
    elif answ in answ_yes:
        return True
    else:
        return False

def ask_for_prefered_resolution():
    t  = f'Type in the preferred resolution ?\n'
    t += ', '.join(pixels)
    t += "\nPress 'q' to quit"
    answ = ask( t ) # Ask for a resolution
    if answ in answ_quit:
        return answ_quit[0]
    elif answ in pixels:
        return answ
    else:
        return '720p'

def ask_for_map():
    t  = 'Choose/make a directory. If a map doesn\'t exists it will be created\n'
    t += 'Press <enter> to use the root-map of the app.\n'
    t += "Press 'q' to quit"
    answ = ask( t ) # Ask for a maps

    if answ in answ_quit:
        return answ_quit[0]
    else: # Process/make dir
        mdir = process_dir( answ )
        return mdir

def ask_another():
    t  = 'Download another file from YouTube ?\n'
    t += "Type 'y' for yes. \n"
    t += "Press <enter> or an other key to quit"
    answ = ask( t )

    return True if answ in answ_yes else False

# App loop
def main():
    while True:
        # Reset default values
        audio, mp3, video = False, False, False
        error, streamaudio, stream_video = False, None, None
        res, adaptive = False, False
        video_path, audio_path = False, False

        # Ask for youtube url ?
        url = ask_yt_url()
        if url in answ_quit: break
        print(f'The downloadurl is: {url}')

        # Ask for audio only ?
        audio = ask_audio_only()
        if audio in answ_quit: break

        if audio: # Only audio
            mp3 = ask_audio_to_mp3() # Ask for convert to mp3
            if mp3 in answ_quit: break
        else: # A video is asked for
            video = True
            res = ask_for_prefered_resolution()
            if res in answ_quit: break

        # Directory handling
        mdir = ask_for_map()
        if mdir in answ_quit: break
        print( f'Selected map is: {mdir}' )


        try: # Get meta info movie parameters
            print(f'\nCheck meta info clip: {url}')
            yt = pytube.YouTube(url)
        except Exception as e:
            print(f'Error in stream:{e}')
            error = True
        else:
            # Print media info
            title = clean_spaces(yt.title)[:100]  # Shortened a bit
            description = clean_spaces(yt.description)[:500] # Shortened
            print(f'Check clip succes.\nTitle: {title}\nDescription\n{description}')

        if not error:
            if video:
                try: # Process video
                    print(f'\nDownload video: {url}.\nTo directory: {mdir}')
                    stream_video, res = get_video(yt, res)
                    if stream_video:
                        print(f'With resolution {stream_video.resolution}')
                        print(f'To directory: {mdir}')
                        video_path = stream_video.download(mdir)
                    else:
                        error = True
                except Exception as e:
                    print(f'Download error in videostream: {stream_video}\n{e}\n')
                    error = True
                else:
                    print(f'Download video successful.\nTo: {video_path}')

                if stream_video.is_adaptive:
                    adaptive = True
                    video_path_new = newname(video_path)
                    rename(video_path, video_path_new)
                    video_path = video_path_new

            if audio or adaptive:
                try: # Process audio
                    print(f'\nDownload audio: {url}\nTo directory: {mdir}')
                    stream_audio = get_audio( yt )
                    if stream_audio:
                        audio_path = stream_audio.download(mdir)
                        print ('Audiopath is', audio_path)
                    else:
                        error = True
                except Exception as e:
                    print(f'Download error in audiostream: {stream_audio}\n{e}\n')
                    error = True
                else:
                    print(f'Download audio successful.\nTo: {audio_path}')

        if not error:
            if adaptive: # Adaptive video, merge video and audio
                try: # Make video clip
                    video_real = oldname(video_path)
                    print('\nMake videoclip, merge video and audio.')
                    print(f'To: {video_real}')
                    video_clip = moviepy.editor.VideoFileClip(video_path)
                    audio_clip = moviepy.editor.AudioFileClip(audio_path)
                    final_clip = video_clip.set_audio(audio_clip)
                    final_clip.write_videofile(video_real)
                    # Remove old files
                    remove(audio_path)
                    remove(video_path)

                except Exception as e:
                    print(f'Error in merging video and audiostream\n{e}')
                    error = True
                else:
                    print(f'Merging video and audiostream successful')
                    answ = open_with_app('Open video file', video_real)
                    if answ in answ_quit: break

            if mp3: # Change audio to mp3
                try: # Make mp3 file
                    base, ext = os.path.splitext(audio_path)
                    audio_real = f'{base}.mp3'
                    print(f'\nConvert clip to mp3 {audio_real}')
                    clip = moviepy.editor.AudioFileClip(audio_path)
                    clip.write_audiofile(audio_real)
                    remove(audio_path) # Remove old file
                except Exception as e:
                    print(f'Error in converting to mp3\n{e}')
                    error = True
                else:
                    print('Audio mp3 created successful')
                    answ = open_with_app('Open music file', audio_real)
                    if answ in answ_quit: break

        if error:
            t = '\nErrors occured...\n'
            if yt.streams:
                strms = '\n'.join(yt.streams)
                t += f'Available streams are {strms}'
            else:
                t += f'No streams found.\nIs {url} correct ?'
            print(t)

        # Another YouTube file ?
        if not ask_another():
            break

     print('\nGood bye...')


if __name__ == '__main__':
    main()

