# -*- coding: utf-8 -*-
'''Text handling'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import re

lst_yes  =  [ 'y', 'yes', 'ok', 'oke', 'j', 'yee' ]
lst_no   =  [ 'n', 'no', 'nee', 'nope', 'nada' ]
lst_quit =  [ 'q', 'stop', 'done' ]

# Available resolutions
lst_pixels    =  ['2160', '1440', '1080', '720', '360', '240', '144']

base_url  =  'https://www.youtube.com/watch?v=' 

def try_again(answ):
    print(f'Given answer {answ}\n')
    print('Not an option !\n')
    print('Try again...')
    
def clean_spaces(s):
    '''Remove unnecessary (double) whitespaces'''
    s = re.sub('\n\n+', '\n', s)
    s = re.sub('\s\s+', ' ', s)
    return s

def quit( s ):
    return str(s).lower() in lst_quit

def show_errors(yt, url):
    t = 'Errors occured...\n'
    if yt.streams:
        strms = '\n'.join(yt.streams)
        t += f'Available streams are {strms}'
    else:
        t += f'No streams found.\nIs {url} correct ?'
    print(t)

