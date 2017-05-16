#!/usr/bin/env python

import glob
import os
import pwd
import grp
import sys
import tarfile
import urllib
from resource_management import *

reload(sys)
sys.setdefaultencoding('utf8')


class Master(Script):
    def install(self, env):
        import params
        env.set_params(params)

        Execute('find ' + params.service_packagedir + ' -iname "*.sh" | xargs chmod +x')
        # create the log, pid, mits dirs
        Directory([params.mist_pid_dir, params.mist_log_dir, params.mist_dir, params.conf_dir],
                  owner=params.mist_user,
                  group=params.mist_group
                  )

        self.create_linux_user(params.mist_user, params.mist_group)
        print 'Install the Mist Master'
        File(params.mist_log_file,
             mode=0644,
             owner=params.mist_group,
             group=params.mist_group,
             content=''
             )
        print 'Getting mist'
        urllib.urlretrieve(params.distribution_url, "/tmp/mist.tar.gz")

        print 'Untar archive'
        tar = tarfile.open("/tmp/mist.tar.gz")
        tar.extractall(path="/tmp")
        tar.close()
        Execute(format("cp -R /tmp/mist/* {mist_dir}"))
        Execute(format("sudo chown -R {mist_user}:hadoop {mist_dir}"))

        # Install packages listed in metainfo.xml
        self.install_packages(env)
        self.configure(env)

        print 'Setup view'
        Execute(format("{service_packagedir}/scripts/setup_view.sh {mist_dir} "
                       "{mist_addr} {mist_port} {setup_view} {service_packagedir} "
                       "{java64_home} >> {mist_log_file}"),
                user=params.mist_user)

        start_script = InlineTemplate(params.mist_ambari_start)
        File(format("{mist_dir}/bin/mist-daemon-start.sh"), content=start_script,
             owner=params.mist_user, group=params.mist_group, mode=0777)
        stop_script = InlineTemplate(params.mist_ambari_stop)
        File(format("{mist_dir}/bin/mist-daemon-stop.sh"), content=stop_script,
             owner=params.mist_user, group=params.mist_group, mode=0777)

        mist_ambari_service = InlineTemplate(params.mist_ambari_service)
        File(format("/etc/init.d/mist"), content=mist_ambari_service,
             owner=params.mist_user, group=params.mist_group, mode=0777)

        if params.setup_view:
            if params.ambari_host == params.mist_internalhost and not os.path.exists(
                    '/var/lib/ambari-server/resources/views/mist-ambari-view-0.0.1.jar'):
                Execute('echo "Copying mist view jar to ambari views dir"')
                Execute(format("cp {mist_dir}/mist-ambari-view-0.0.1.jar "
                               "/var/lib/ambari-server/resources/views"), ignore_failures=True)

    def configure(self, env):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        mist_default = InlineTemplate(status_params.mist_default_template_config)
        File(format("{conf_dir}/default.conf"), content=mist_default, owner=params.mist_user, group=params.mist_group, mode=0644)

        mist_routers = InlineTemplate(status_params.mist_routers_template_config)
        File(format("{conf_dir}/router-examples.conf"), content=mist_routers, owner=params.mist_user, group=params.mist_group, mode=0644)

    def stop(self, env):
        import params

        self.configure(env)
        Execute(format("{mist_dir}/bin/mist-daemon-stop.sh"), user=params.mist_user)
    def start(self, env):
        import params

        self.configure(env)
        print 'Start the Mist Master'
        Execute(format("{mist_dir}/bin/mist-daemon-start.sh"), user=params.mist_user)

        pidfile = glob.glob(params.mist_pid_file)[0]
        Execute('echo pid file is: ' + pidfile, user=params.mist_user)
        contents = open(pidfile).read()
        Execute('echo pid is ' + contents, user=params.mist_user)

    def status(self, env):
        import status_params
        env.set_params(status_params)

        pid_file = glob.glob(status_params.mist_pid_file)[0]
        check_process_status(pid_file)
    def create_linux_user(self, user, group):
        try:
            pwd.getpwnam(user)
        except KeyError:
            Execute('adduser ' + user)
        try:
            grp.getgrnam(group)
        except KeyError:
            Execute('groupadd ' + group)


if __name__ == "__main__":
    Master().execute()
