Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |config|
    config.memory = 2048
    config.cpus = 2
  end

  config.vm.define "ambari" do |ambari|
    ambari.vm.host_name = 'ambari'
    ambari.vm.network "private_network", ip: "192.168.56.50"
  end
end
