# -*- coding: utf-8 -*-
'''File for default and config variables '''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

# Defaults in questions 
ask_default_resolution     = '720'  # Default video resolution in px
# Progressive (audio and video in one file) only availabele for video's
# with a resolution <= 720px
ask_default_progressive    = 'n'     # Download video and audio separate for higher quality
ask_default_audio_only     = 'n'     # Only audio
ask_default_audio_to_mp3   = 'y'     # Convert audio to mp3 (in the audio only option)
ask_default_download_again = 'y'     # Default option for another download
ask_default_open_with_app  = 'y'     # Default option for open with an (default) app on your OS
