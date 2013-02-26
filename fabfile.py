# coding: utf-8
import os

from fabric.api import *

env.user = 'vagrant'
env.port = 2222
env.key_filename = '/Users/rcmachado/.vagrant.d/insecure_private_key'
env.hosts = ['127.0.0.1']

LOCAL_DIR = os.path.dirname(__file__)
PROJECT_DIR = '/var/www/project/'


@task
def setup():
    packages = 'nginx python python-pip'

    with prefix('DEBIAN_FRONTEND=noninteractive'):
        sudo('apt-get update')
        sudo('apt-get -y install {}'.format(packages))

    sudo('mkdir -p {}'.format(PROJECT_DIR))

    sudo('pip install virtualenv')
    sudo('virtualenv {}virtualenv'.format(PROJECT_DIR))

    install_requirements()
    put(os.path.join(LOCAL_DIR, 'deploy', 'upstart.conf'),
        '/etc/init/mybookmarks.conf', use_sudo=True)
    put(os.path.join(LOCAL_DIR, 'deploy', 'nginx-site.conf'),
        '/etc/nginx/sites-enabled/mybookmarks.conf', use_sudo=True)
    sudo('rm -f /etc/nginx/sites-enabled/default')
    execute(nginx, 'restart')


def install_requirements():
    requirements = os.path.join(LOCAL_DIR, 'requirements.txt')
    python_packages = open(requirements).read().replace('\n', ' ')
    sudo('{}virtualenv/bin/pip install {}'.format(PROJECT_DIR, python_packages))


@task
def deploy():
    sudo('rm -rf {}mybookmarks'.format(PROJECT_DIR))
    put(os.path.join(LOCAL_DIR, 'mybookmarks'), PROJECT_DIR, use_sudo=True)
    execute(restart)


@task
def start():
    sudo('start mybookmarks')


@task
def stop():
    sudo('stop mybookmarks')


@task
def restart():
    with settings(warn_only=True):
        execute(stop)
    execute(start)


@task
def nginx(op):
    sudo('service nginx {}'.format(op))
