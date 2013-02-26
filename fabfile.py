# coding: utf-8
import os

import boto

LOCAL_DIR = os.path.dirname(__file__)
boto.config.load_from_path(os.path.join(LOCAL_DIR, 'deploy', 'boto.cfg'))

from fabric.api import *
from fabix.aws import ec2


PROJECT_DIR = '/var/www/project/'


@task
def prod():
    """Configure env variables for production"""
    env.user = 'ubuntu'
    env.key_filename = '/path/to/key.pem'
    env.hosts = ec2.get_autoscaling_instances('mybookmarks-app')


@task
def setup():
    """Setup project"""
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
def setup_autoscale():
    """Setup AWS autoscale"""
    kwargs = {
        "ami_id": 'ami-3fec7956',  # Official Ubuntu 12.04.1 LTS US-EAST-1
        "instance_type": "t1.micro",
        "key_name": "mybookmarks",
        "security_groups": ["mybookmarks-app"],
        "availability_zones": ["us-east-1a", "us-east-1b", "us-east-1c"],
        "min_instances": 1,
        "sp_up_adjustment": 2,
        "load_balancers": ["mybookmarks-app"]
    }
    ec2.setup_autoscale('mybookmarks-app', **kwargs)


@taks
def update_autoscale(instance_id):
    """Update autoscale configuration"""
    ec2.update_autoscale(instance_id, 'mybookmarks-app')


@task
def deploy():
    """Deploy project to server"""
    sudo('rm -rf {}mybookmarks'.format(PROJECT_DIR))
    put(os.path.join(LOCAL_DIR, 'mybookmarks'), PROJECT_DIR, use_sudo=True)
    execute(restart)


@task
def start():
    """Start application service"""
    sudo('start mybookmarks')


@task
def stop():
    """Stop application service"""
    sudo('stop mybookmarks')


@task
def restart():
    """Stop and start application service"""
    with settings(warn_only=True):
        execute(stop)
    execute(start)


@task
def nginx(op):
    """Manage nginx service"""
    sudo('service nginx {}'.format(op))
