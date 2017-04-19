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

  def stop(self, env):
    print 'Stop the Sample Srv Master';
    Execute ('cd /usr/share/mist/; SPARK_HOME=${SPARK_HOME} bin/mist stop')

  def start(self, env):
    print 'Start the Sample Srv Master';
    Execute ('cd /usr/share/mist/; SPARK_HOME=${SPARK_HOME} bin/mist start master')

  def status(self, env):
    print 'Status of the Sample Srv Master';

  def configure(self, env):
    print 'Configure the Sample Srv Master';

if __name__ == "__main__":
  Master().execute()
