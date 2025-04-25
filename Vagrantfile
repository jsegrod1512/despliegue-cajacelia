VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/focal64"
  config.ssh.insert_key = false

  # Server Web (DMZ)
  config.vm.define "webserver" do |node|
    node.vm.hostname = "webserver"
    node.vm.network "private_network", ip: "10.1.0.10", virtualbox__intnet: "DMZ"
  end

  # Servidor CI/CD con Jenkins (LAN)
  config.vm.define "ci-cd" do |node|
    node.vm.hostname = "ci-cd"
    node.vm.network "private_network", ip: "172.16.1.10", virtualbox__intnet: "LAN"
  end

  # Servidor de Base de Datos (LAN)
  config.vm.define "database" do |node|
    node.vm.hostname = "database"
    node.vm.network "private_network", ip: "172.16.1.11", virtualbox__intnet: "LAN"
  end

  # Servidor de Autenticación LDAP (LAN)
  config.vm.define "ldap" do |node|
    node.vm.hostname = "ldap"
    node.vm.network "private_network", ip: "172.16.1.12", virtualbox__intnet: "LAN"
  end

  # Cliente Ubuntu Desktop (LAN, DHCP)
  config.vm.define "client" do |node|
    node.vm.box = "ubuntu/bionic64-desktop"
    node.vm.hostname = "client"
    node.vm.network "private_network", type: "dhcp", virtualbox__intnet: "LAN",
    node.vm.provider "virtualbox" do |vb|
      vb.gui = true
      vb.memory = 2048
    end
  end

#   # Provisioning con Ansible
#   config.vm.provision "ansible" do |ansible|
#     ansible.playbook = "site.yml"
#     ansible.inventory_path = "inventory/inventory"
#     ansible.limit = "all"
#   end
end
