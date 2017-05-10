#!/usr/bin/env python

import sys, os, pwd, signal, time
import urllib, tarfile
from resource_management import *
from subprocess import call

class Master(Script):

  def install(self, env):
    print 'Install the Sample Srv Master';
    # Install packages listed in metainfo.xml
    self.install_packages(env)

    print 'Getting mist'
    urllib.urlretrieve ("http://35.157.13.60/mist.tar.gz", "/tmp/mist.tar.gz")

    print 'Untar archive'
    tar = tarfile.open("/tmp/mist.tar.gz")
    tar.extractall(path="/usr/share")
    tar.close()

    print 'Create Mist service'
    Execute ('cp /var/lib/ambari-server/resources/stacks/HDP/2.5/services/MIST/package/scripts/mist_service.sh /etc/init.d/mist')
    Execute ('chmod +x /etc/init.d/mist')


  def stop(self, env):
    print 'Stop the Sample Srv Master';
    Execute ('service mist stop')

  def start(self, env):
    print 'Start the Sample Srv Master';
    Execute ('service mist start')

  def status(self, env):
    import status_params
    env.set_params(status_params)

    pid_file = glob.glob(status_params.mist_pid_dir + '/mist.pid')[0]
    check_process_status(pid_file)

  def configure(self, env):
    print 'Configure the Sample Srv Master';

if __name__ == "__main__":
  Master().execute()
