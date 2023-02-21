import os
from pathlib import Path

home_directory = os.path.expanduser( '~' )
Python_path =  Path.home()
print( home_directory )
print( Python_path )
print("HEYOLOOOO Training")