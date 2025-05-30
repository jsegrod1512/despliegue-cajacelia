Vagrant.configure("2") do |config|
  # Deshabilita el montaje automático de /vagrant en todas las VMs
  config.vm.synced_folder ".", "/vagrant", disabled: true

  # Usa Ubuntu Server LTS por defecto
  config.vm.box = "ubuntu/focal64"
  
  # Genera una clave SSH distinta para cada VM (mejor seguridad)
  config.ssh.insert_key = true

  # # 0) pfSense
  # config.vm.define "pfsense" do |node|
  #   node.vm.box = "pfsense"
  #   node.vm.hostname = "pfsense"
  #   node.vm.network "public_network",
  #     type: "dhcp",
  #     bridge: "wlo1"
  #   node.vm.network "private_network",
  #     ip: "172.16.1.1",
  #     virtualbox__intnet: "LAN"
  #   node.vm.network "private_network",
  #     ip: "10.1.0.1",
  #     virtualbox__intnet: "DMZ"
  #   node.vm.provider "virtualbox" do |vb|
  #     vb.name   = "pfSense"
  #     vb.memory = 2048
  #   end

  #   node.vm.synced_folder "./templates", "/vagrant/templates", type: "virtualbox"

  #   node.vm.provision "shell", privileged: true, inline: <<-SHELL
  #     cp /vagrant/templates/config-pfsense.cajacelia.es /conf/config.xml
  #     touch /conf/needs_config_restore
  #     reboot
  #   SHELL
  # end

  # 1) VM en DMZ: webserver
  config.vm.define "webserver" do |node|
    node.vm.hostname = "webserver"
    node.vm.network "private_network",
      ip: "10.1.0.10",
      virtualbox__intnet: "DMZ"      # internal network DMZ 
    # default router
    node.vm.provision "shell",
      run: "always",
      inline: <<-SHELL
        # Verificar si la ruta por defecto ya existe
        if ! ip route | grep -q '^default via 10.1.0.1'; then
          ip route add default via 10.1.0.1
        fi
      SHELL
    node.vm.provider "virtualbox" do |vb|
      vb.name = "Webserver" 
      vb.memory = 1024
    end
  end

  # 2) VM en LAN: Base de datos
  config.vm.define "database" do |node|
    node.vm.hostname = "database"
    node.vm.network "private_network",
      ip: "172.16.1.11",
      virtualbox__intnet: "LAN"
    # default router
    node.vm.provision "shell",
      run: "always",
      inline: <<-SHELL
        # Verificar si la ruta por defecto ya existe
        if ! ip route | grep -q '^default via 172.16.1.1'; then
          ip route add default via 172.16.1.1
        fi
      SHELL
    node.vm.provider "virtualbox" do |vb|
      vb.name = "Database"
      vb.memory = 1024
    end
  end

  # 3) VM en LAN: LDAP
  config.vm.define "ldap" do |node|
    node.vm.hostname = "ldap"
    node.vm.network "private_network",
      ip: "172.16.1.12",
      virtualbox__intnet: "LAN"
    # default router
    node.vm.provision "shell",
    run: "always",
    inline: <<-SHELL
      # Verificar si la ruta por defecto ya existe
      if ! ip route | grep -q '^default via 172.16.1.1'; then
        ip route add default via 172.16.1.1
      fi
    SHELL
    node.vm.provider "virtualbox" do |vb|
      vb.name = "LDAP"
      vb.memory = 1024
    end
  end

  # 4) VM Cliente Ubuntu Desktop (LAN, DHCP)
  config.vm.define "client" do |node|
    node.vm.box = "gusztavvargadr/ubuntu-desktop"
    node.vm.box_version = "2404.0.2503"
    node.vm.hostname = "client"
    node.vm.network "private_network",
      type: "dhcp",
      virtualbox__intnet: "LAN"
    node.vm.provider "virtualbox" do |vb|
      vb.name = "Client"
      vb.memory = 2048
      vb.gui = true
    end
  end

  # 5) VM en LAN: CI/CD (Jenkins)
  config.vm.define "ci-cd" do |node|
    node.vm.hostname = "ci-cd"
    node.vm.network "private_network",
      ip: "172.16.1.10",
      virtualbox__intnet: "LAN"
    # default router
    node.vm.provision "shell",
    run: "always",
    inline: <<-SHELL
      # Verificar si la ruta por defecto ya existe
      if ! ip route | grep -q '^default via 172.16.1.1'; then
        ip route add default via 172.16.1.1
      fi
    SHELL
    node.vm.provider "virtualbox" do |vb|
      vb.name = "CI-CD"
      vb.memory = 2048
    end

    node.vm.synced_folder ".", "/vagrant", type: "virtualbox"
      
    node.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "/vagrant/site.yml"
      ansible.raw_arguments = ["--timeout=400"]
      # ansible.inventory_path   = "/vagrant/inventory"
      ansible.inventory_path = "/vagrant/inventory"
      ansible.provisioning_path = "/vagrant"
      ansible.limit = "all"
      ansible.verbose = true
    end
  end
end
