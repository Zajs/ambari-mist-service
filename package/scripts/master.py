#!/usr/bin/env python

import sys, os, pwd, signal, time
import urllib, tarfile
from resource_management import *
from subprocess import call

class Master(Script):

  def install(self, env):
    import params
    env.set_params(params)

    print 'Install the Mist Master';
    # Install packages listed in metainfo.xml
    self.install_packages(env)

    Execute('find ' + params.service_packagedir + ' -iname "*.sh" | xargs chmod +x')

   # create the log, pid, mits dirs
    Directory([params.mist_pid_dir, params.mist_log_dir, params.mist_dir],
              owner=params.mist_user,
              group=params.mist_group,
              recursive=True
              )

    print 'Getting mist'
    urllib.urlretrieve ("http://35.157.13.60/mist.tar.gz", "/tmp/mist.tar.gz")

    print 'Untar archive'
    tar = tarfile.open("/tmp/mist.tar.gz")
    tar.extractall(path="/usr/share")
    tar.close()

    print 'Create Mist service'
    Execute ('cp /var/lib/ambari-server/resources/stacks/HDP/2.5/services/MIST/package/scripts/mist_service.sh /etc/init.d/mist')
    Execute ('chmod +x /etc/init.d/mist')

    Execute(format("{service_packagedir}/scripts/setup_snapshot.sh {mist_dir} "
                   "{mist_host} {mist_port} {setup_view} {service_packagedir} "
                   "{java64_home} >> {mist_log_file}"),
            user=params.mist_user)

    # if zeppelin installed on ambari server, copy view jar into ambari views dir
    if params.setup_view:
        if params.ambari_host == params.mist_internalhost and not os.path.exists(
                '/var/lib/ambari-server/resources/views/mist-view-1.0-SNAPSHOT.jar'):
            Execute('echo "Copying mist view jar to ambari views dir"')


            Execute(format("cp /var/lib/ambari-server/resources/stacks/HDP/2.5/services/MIST/package/scripts/*.jar "
                           "/var/lib/ambari-server/resources/views"), ignore_failures=True)
            #Execute(format("cp /home/zeppelin/*.jar "
            #               "/var/lib/ambari-server/resources/views"), ignore_failures=True)


  def stop(self, env):
    print 'Stop the Mist Master';
    Execute ('service mist stop')

  def start(self, env):
    print 'Start the Mist Master';
    Execute ('service mist start')

  def status(self, env):
    import status_params
    env.set_params(status_params)

    pid_file = glob.glob(status_params.mist_pid_dir + '/mist.pid')[0]
    check_process_status(pid_file)

  def configure(self, env):
    print 'Configure the Mist Master';

if __name__ == "__main__":
  Master().execute()
