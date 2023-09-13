# -*- coding: utf-8 -*-
'''Ask functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import sources.txt as txt

def question(t, quit=False, yes=False, no=False, default=''): 
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
    t  = 'Give/paste a complete youtube URL.\n'
    t += 'Or put only the ID-part in the url /watch?v=<ID>'
    answ = question(t, quit=True)

    if answ in txt.lst_quit:
        return txt.lst_quit[0]
    else:
        # If only id is given, add base url
        if 'https://' not in answ and 'http://' not in answ: 
            answ = f'{txt.base_url}{answ}'
        else: 
            # Complete url given. No checks for now
            pass

    print(f'\nThe given downloadurl is:')
    print(f'"{answ}"')
    return answ 


def audio_only(default):
    answ = ''
    while True:
        t  = 'Download audio only ?'
        answ = question(t, quit=True, yes=True, no=True, default=default)

        if answ in txt.lst_quit:
            return txt.lst_quit[0]
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


def audio_to_mp3(default):
    answ = ''
    while True:
        t  = f'Do you want to change the media file to a mp3 file ?'
        answ = question(t, quit=True, yes=True, no=True, default=default)

        if answ in txt.lst_quit: 
            return txt.lst_quit[0]
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


def video_resolution(default):
    while True:
        t  = f'Give the preferred resolution (px) ?\n'
        t += ', '.join(txt.lst_pixels)
        answ = question(t, quit=True, default=default)

        if answ in txt.lst_quit: 
            return txt.lst_quit[0]
        elif answ in txt.lst_pixels: 
            answ = answ + 'p' # Always add p
            print(f'\nVideo resolution is: {answ}')
            return answ
        
        txt.try_again(answ)


def download_map(default):
    t  = 'Give a download map name in the application map ?'
    answ = question(t, quit=True, default=default) # Ask for a maps

    if answ in txt.lst_quit: 
        return txt.lst_quit[0]

    print('\nSelected downloadmap is:')
    print(f'"{answ}"')
    return answ

def download_again(default):

    while True:
        t  = 'Download another file from YouTube ?\n'
        t += "Press <enter> for yes." 
        answ = question(t, quit=False, yes=True, no=True, default=default)

        if answ in txt.lst_yes:
            return True
        elif answ in txt.lst_no:
            return False   
        
        print('Press "y" for yess or "n" for no...\n')


def open_with_app(path, default):
    '''Ask for opening a downloaded media file'''
    t  = 'Open file ?\n'
    t += f'"{path}"\n' 
    t += 'With a default app ?'
    answ = question( t, quit=False, yes=True, no=True, default=default ) 

    if answ in txt.lst_yes: 
        return True 
    elif answ in txt.lst_no: 
        return False 
