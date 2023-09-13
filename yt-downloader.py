# -*- coding: utf-8 -*-
'''Program downloads an video/mp3 from youtube based on an id or a complete url'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

#  Use: python version >= 3.7
#  Install modules with: 
#  python3 -m pip install -r requirements.txt
#  If url from share copy does not work, try to copy the youtube url in the browser
#  Update used modules e.g. pytube with:
#  python3 -m pip install pytube --upgrade

import os
import sources.ask as ask 
import sources.txt as txt
import sources.fn as fn

# Are python modules installed ?
fn.check_for_modules() 

app_map = os.path.dirname(os.path.abspath(__file__))
audio_map = os.path.join(app_map, 'audio')
video_map = os.path.join(app_map, 'video')

if __name__ == '__main__': 
    while True: # App loop
        # Init/Reset default values
        ok, audio_only, mp3, video = False, False, False, True
        video_res, adaptive, video_path, audio_path = False, True, False, False 
        stream_audio, stream_video = None, None
        media_path, download_map = '', ''

        # Ask for youtube url ?
        url = ask.yt_url()
        if txt.quit(url): 
            break

        # Ask for audio only ?
        audio_only = ask.audio_only(default='n')
        if txt.quit(audio_only): 
            break
        
        if audio_only: # Only audio
            # Set video to false and ask for to convert to mp3
            video, mp3 = False, ask.audio_to_mp3(default='n') 
            if txt.quit(mp3): 
                break
        else: # A video is asked for (too), not audio only
            video_res = ask.video_resolution(default='1080') # Ask for a video resolution
            if txt.quit(video_res): 
                break

        # Process youtube url
        ok, yt, title, description = fn.youtube(url) 

        if ok: # No errors (yet)

            # Download audio
            ok, audio_path = fn.process_audio(yt, url, audio_map)
            if ok:
                if mp3: 
                    # Change audio to mp3 
                    ok, audio_path = fn.audio_to_mp3(audio_path)
                    if not ok: 
                        break 
            else:
                break
            
            # Download video too if not audio only
            if not audio_only:
                ok, video_path = fn.process_video(yt, url, video_map, video_res)
                if ok:
                    # Now merge video and audio
                    ok, media_path = fn.merge_video_and_audio(video_path, audio_path)
                    if not ok:
                        break
                else:
                    break
            else:
                media_path = audio_path

        else:
            break

        if not ok: # Something went wrong
            txt.show_errors(yt, url)
        else:
            if ask.open_with_app(media_path, default="y"):
                ok = fn.exec_with_app(media_path)

        # Another YouTube file ?
        if ask.download_again(default='n'):
            continue
        else:
            break # End

    print('\nGood bye.')
