#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack
"""

from fabric.api import local
from datetime import datetime

def do_pack():
    """
    function to generate .tgz archive
    """

    #create versions folder if it doesn't exist
    local("mkdir -p versions")

    #generate archive name based on current date and time
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

    #compress content of web_static folder into a .tgz archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    #check if archive was successfully generated
    if result.failed:
        return None
    else:
        return ("versions/{}".format(archive_name))
