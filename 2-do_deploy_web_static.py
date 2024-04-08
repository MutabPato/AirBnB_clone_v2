#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from fabric.api import local, put, run, env
from datetime import datetime
from os.path import exists

env.hosts = ['52.87.255.220', '3.89.146.3']


def do_pack():
    """
    function to generate .tgz archive
    """

    # create versions folder if it doesn't exist
    local("mkdir -p versions")

    # generate archive name based on current date and time
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

    # compress content of web_static folder into a .tgz archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # check if archive was successfully generated
    if result.failed:
        return None
    else:
        return ("versions/{}".format(archive_name))


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not exists(archive_path):
        print("Archive does not exist.")
        return False

    try:
        # extract necessary information from archive path
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        # upload to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # create necessary directories and extract archive
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))

        # clean up and create symbolic link
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        print("New version deployed successfully!")
        return True

    except Exception as e:
        print("Error deploying archive:", e)
        return False
