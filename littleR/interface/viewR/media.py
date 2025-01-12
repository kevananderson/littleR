import os
import hashlib
import shutil

from django.conf import settings
from .models import Standard_Model as Std

def hash_file(file_path):
    """Get the hash of a file."""
    # open the file
    with open(file_path, "rb") as file:
        # create the hash object
        file_hash = hashlib.sha256()
        
        # read the file in chunks
        for chunk in iter(lambda: file.read(4096), b""):
            file_hash.update(chunk)
    
    # return the hash
    return file_hash.hexdigest()

def logo():
    """Get the logo for the viewR app."""
    # get the standard
    standard = Std.model()

    # get the logo path and hash
    logo_path = standard.config.get_logo()
    if logo_path == "":
        return False
    logo_hash = hash_file(logo_path)
    
    #logo directory and path
    logo_media_dir = os.path.join( settings.BASE_DIR , 'viewR/static/viewR/img').replace("\\","/")
    logo_media_path = os.path.join(logo_media_dir, 'project_logo.png').replace("\\","/")

    # check if the logo is in the media directory
    if not os.path.isfile(logo_media_path) or logo_hash != hash_file(logo_media_path):
        # copy the logo to the media directory
        shutil.copy2(logo_path, logo_media_path)

    # return the logo path
    return True


    
