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
import sources.txt as txt

def question(t, quit=False, yes=False, no=False, default=''):
    '''Ask for an user input''' 
    q = f'\n{t}\n' 
    if yes:     q += 'Type "y" for yes\n' 
    if no:      q += 'Type "n" for no\n' 
    if default: q += f'Press <enter> for default "{default}" \n'
    if quit:    q += 'Press "q" to quit\n' 
    q += ' ? \n'

    answ = input(q).strip()

    if not answ and default:
        answ = default

    return answ

def yt_url():
    '''Ask for a YouTube video url'''
    t  = 'Give/paste a complete youtube URL.\n'
    t += 'Or put only the ID-part in the url /watch?v=<ID>'
    answ = question(t, quit=True)

    if txt.is_quit(answ):
        return txt.quit
    else:
        # If only id is given, add base url
        if 'https://' not in answ and 'http://' not in answ: 
            answ = f'{txt.base_url}{answ}'
        else: 
            # Complete url given. 
            # No url checks for now
            pass

    print(f'\nThe given downloadurl is:')
    print(f'"{answ}"')
    return answ 


def progressive(default=cfg.ask_default_progressive):
    '''Ask to download a audo and a video file separately'''
    answ = ''
    while True:
        t  = 'Do you want to download a separate video and an audio file ? \n'
        t += 'The separation of a video and audio file, gives a much higher quality (mostly in sound).\n'
        t += 'But it will take a lot longer to process the video.\n'
        t += 'A video with the audio and video in one file is only available for video\'s with a 720px resolution or lower.\n'
        t += 'For a higher resolution (>720px), you always must chose the separate files option.' 
        answ = question(t, quit=True, yes=True, no=True, default=default)

        if txt.is_quit(answ):
            return txt.quit
        else:
            if answ in txt.lst_yes:
                answ = True
            elif answ in txt.lst_no:
                answ = False
            else:
                txt.try_again(answ)
                continue
        break

    print(f'\nProgressive video is: {answ}')
    return answ


def audio_only(default=cfg.ask_default_audio_only):
    '''Ask to only download an audio file'''
    answ = ''
    while True:
        t  = 'Download audio only ?'
        answ = question(t, quit=True, yes=True, no=True, default=default)

        if txt.is_quit(answ):
            return txt.quit
        else:
            if answ in txt.lst_yes:
                answ = True
            elif answ in txt.lst_no:
                answ = False
            else:
                txt.try_again(answ)
                continue
        break

    print(f'\nAudio only is: {answ}')
    return answ


def audio_to_mp3(default=cfg.ask_default_audio_to_mp3):
    '''Ask to convert an audio file to a mp3 file'''
    answ = ''
    while True:
        t  = f'Do you want to change the media file to a mp3 file ?'
        answ = question(t, quit=True, yes=True, no=True, default=default)

        if txt.is_quit(answ):
            return txt.quit
        else:
            if answ in txt.lst_yes:
                answ = True
            elif answ in txt.lst_no:
                answ = False
            else:
                txt.try_again(answ)
                continue
        break

    print(f'\nConvert audio to mp3 is: {answ}')
    return answ


def video_resolution(default=cfg.ask_default_resolution):
    '''Ask for a video resolution'''
    answ = ''
    while True:
        t  = f'Give the preferred resolution (px) ?\n'
        t += ', '.join(txt.lst_pixels)
        answ = question(t, quit=True, default=default)

        if txt.is_quit(answ):
            return txt.quit
        elif answ in txt.lst_pixels: 
            answ = answ + 'p' # Always add p
        else:
            txt.try_again(answ)
            continue 
        break

    print(f'\nVideo resolution is: {answ}')
    return answ

def download_again(default=cfg.ask_default_download_again):
    '''Ask to download another file from Youtube'''
    while True:
        t  = 'Download another file from YouTube ?\n'
        t += "Press <enter> for yes." 
        answ = question(t, quit=False, yes=True, no=True, default=default)

        if txt.is_quit(answ):
            return False
        elif answ in txt.lst_yes:
            return True
        elif answ in txt.lst_no:
            return False

def open_with_app(path, default=cfg.ask_default_open_with_app):
    '''Ask for opening a downloaded media file'''
    t  = 'Open file ?\n'
    t += f'"{path}"\n' 
    t += 'With a default app ?'
    answ = question( t, quit=False, yes=True, no=True, default=default ) 

    if txt.is_quit(answ):
        return txt.quit
    elif answ in txt.lst_yes: 
        return True 
    elif answ in txt.lst_no: 
        return False 
