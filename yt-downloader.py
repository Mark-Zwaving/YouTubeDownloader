# -*- coding: utf-8 -*-
'''Program downloads an video/mp3 from youtube based on an id or a complete url'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

#  Use: python version >= 3.7
#  Install modules with: 
#  python3 -m pip install -r requirements.txt
#  If url from share copy does not work, try to copy the youtube url in the browser
#  Update used modules e.g. pytube with:
#  python3 -m pip install pytube --upgrade

import os
import config as cfg
import sources.ask as ask 
import sources.txt as txt
import sources.fn as fn

# ERROR in audiostream: get_throttling_function_name: could not find match for multiple
# LOOK for file: cipher.py (in pytube)
# SEARCH for function: def get_throttling_function_name(js: str)
# REPLACE array: function_patterns = [ .... ]
# WITH: 
# function_patterns = [
#     r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
#     r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
#     r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
# ]
# See source: https://github.com/pytube/pytube/issues/1954 


# Are python modules installed ?
fn.check_for_modules() 

app_map = os.path.dirname(os.path.abspath(__file__))
audio_map = os.path.join(app_map, 'audio')
video_map = os.path.join(app_map, 'video')

if __name__ == '__main__': 
    while True: # App loop
        # Init/Reset default values
        ok, audio_only, mp3, separate, video_path, audio_path = False, False, False, False, False, False 
        resolution, media_path = cfg.ask_default_resolution, ''

        # Ask for youtube url ?
        url = ask.yt_url()
        if txt.is_quit(url): 
            break

        # Ask for audio only ?
        audio_only = ask.audio_only()
        if txt.is_quit(audio_only): 
            break
        
        if audio_only: # Only audio
            # Ask for to convert to mp3
            mp3 = ask.audio_to_mp3() 
            if txt.is_quit(mp3): 
                break
        
        else: # A video is asked for (too), not audio only
            # Progressive video
            separate = ask.progressive()
            if txt.is_quit(separate): 
                break

            resolution = ask.video_resolution() # Ask for a video resolution
            if txt.is_quit(resolution): 
                break

            separate, resolution = fn.check_input_vars(separate, resolution)

        # Process youtube url, raise and catch errors
        try:
            ok, yt, title, description = fn.youtube(url) 
            if ok: # No errors (yet)
                
                if audio_only: # Download audio only
                    # Download audio
                    ok, audio_path = fn.process_audio_only(yt, url, audio_map)
                    if ok:
                        if mp3: # Change audio to mp3 
                            ok, mp3_path = fn.audio_to_mp3(audio_path)
                            if ok:
                                audio_path = mp3_path
                            else: 
                                print('Error in audio to mp3 convertion')
                    else:
                        print('Error processing audio from YouTube')

                    if ok:
                        media_path = audio_path 

                else:
                    try_video_audio = False
                    if not separate:
                        # Download video and audio in one file
                        ok, video_path = fn.process_video_and_audio(yt, url, video_map, resolution)
                        if ok:
                            media_path = video_path 
                        else:
                            print('Processing video and audio in one file from YouTube failed.')
                            print('Now trying to download separate video and audio files...\n')
                            separate = True
                            try_video_audio = True

                    if separate: 
                        # Download audio file
                        ok_audio, audio_path = fn.process_audio_only(yt, url, audio_map) # Download audio
                        if not ok_audio:
                            print('Error processing audio')

                        # Download video file
                        ok_video, video_path = fn.process_video_only(yt, url, video_map, resolution) # Download video
                        if not ok_video:
                            print('Error processing video')

                        ok = ok_video and ok_audio

                        if ok: 
                            ok, video_path = fn.merge_video_and_audio(video_path, audio_path)
                            if ok:
                                media_path = video_path
                            else: 
                                print('Error in merge video and audio')
                        else: 
                            print('Error processing a separate video or audio')
                            if not try_video_audio:
                                # Download video and audio in one file
                                print('Try to download video and audio in one file.')
                                ok, video_path = fn.process_video_and_audio(yt, url, video_map, resolution)
                                if ok:
                                    media_path = video_path
                                else:
                                    print('Processing video and audio in one file from YouTube failed.')
            else:
                print('Fatal error in processing youtube url')

   
        except Exception as e:
            txt.show_errors(yt, url)
            print(f'Error(s)\n{repr(e)}')

        if ok: # No errors somehow ;)
            answ = ask.open_with_app(media_path)
            if txt.is_quit(answ):
                break
            elif answ == True:
                ok = fn.exec_with_app(media_path)

        else:
            print('\nFailed to download a media file from YouTube.\n')

        # Another YouTube file ?
        if ask.download_again() == True:
            continue
        else:
            break # End

    print('\nGood bye.')
