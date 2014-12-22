vw-discover-media-audio-conformer
=================================

Small python script that makes audio files conform to playing on the VW Discover Media audio system.
VW Discover Media supports cover art with a max resolution of 400x400 px.
Also, files starting with a '.' (unix hidden files) are displayed in the song picker.

This script tries to remedy these cases by:
* resizing the front cover to 400x400 px if it is not already at that size
* removing any hidden files
* removing special OSX hidden directories such as .Spotlight-V100 and .Trashes

It uses the mutagen audio manipulation and pillow image manipulation python libraries.
Only files using the mpeg 4 container (m4a) are supported, but mp3 support is possible, as mutagen can handle it.

    $ python conformer.py 
    usage: conformer.py [-h] [--remove-hidden-files]
                        [--remove-osx-special-directories]
                        directory