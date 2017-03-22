#!/usr/bin/env python

import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call


class Master(Script):
  def install(self, env):
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    self.configure(env)

    cmd = 'ps aux'
    Execute(cmd)

if __name__ == "__main__":
  Master().execute()
