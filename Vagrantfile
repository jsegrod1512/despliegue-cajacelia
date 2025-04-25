Vagrant.configure("2") do |config|
  # Usa Ubuntu Server LTS por defecto
  config.vm.box = "ubuntu/focal64"
  # Genera una clave SSH distinta para cada VM (mejor seguridad)
  config.ssh.insert_key = true

  # 1) VM en DMZ: webserver
  config.vm.define "webserver" do |node|
    node.vm.hostname = "webserver"
    node.vm.network "private_network",
      ip: "10.1.0.10",
      virtualbox__intnet: "DMZ"      # internal network DMZ :contentReference[oaicite:0]{index=0}
    node.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end
  end

  # 2) VM en LAN: Base de datos
  config.vm.define "database" do |node|
    node.vm.hostname = "database"
    node.vm.network "private_network",
      ip: "172.16.1.11",
      virtualbox__intnet: "LAN"
  end

  # 3) VM en LAN: LDAP
  config.vm.define "ldap" do |node|
    node.vm.hostname = "ldap"
    node.vm.network "private_network",
      ip: "172.16.1.12",
      virtualbox__intnet: "LAN"
  end

  # 4) VM en LAN: CI/CD (Jenkins)
  config.vm.define "ci-cd" do |node|
    node.vm.hostname = "ci-cd"
    node.vm.network "private_network",
      ip: "172.16.1.10",
      virtualbox__intnet: "LAN"
  
    # Provisionamiento LOCAL de Ansible
    node.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "site.yml"
      ansible.inventory_path = "inventory/inventory"      # Donde están tus playbooks (.yml)
    end
  
    node.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.gui    = false
    end
  end

  # 5) VM Cliente Ubuntu Desktop (LAN, DHCP)
  config.vm.define "client" do |node|
    node.vm.box = "ubuntu/jammy64"
    node.vm.hostname = "client"
    node.vm.network "private_network",
      type: "dhcp",
      virtualbox__intnet: "LAN"
    node.vm.provider "virtualbox" do |vb|
      vb.gui    = true
      vb.memory = 2048
    end
  end
end
