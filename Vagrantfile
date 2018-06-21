# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'
settings = YAML.load_file 'vagrant.yml'

# settings['datacenters'].each do |dc|
#   dc['servers'].each do |machine|
#     txt = "----------- Router: " + dc['name'] + '-' + machine['name']
#     if machine['is_router']
#       puts txt
#     end
#   end
# end

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  # Loop through datacenters
  settings['datacenters'].each do |dc|

    # Loop through servers
    dc['servers'].each do |machine|

      # Variables
      vm_group = '/' + settings['group'] + "/" + dc['name']
      vm_name = settings['group'] + "-" + dc['name'] + '-' + machine['name']
      vm_dc_internal_network = settings['group'] + "-" + dc['name'] + '-network'
      vm_router_network = settings['group'] + '-router-network'
      vm_internal_network = settings['group'] + '-network'

      # Define settings for each node
      config.vm.define vm_name do |node|

        node.vm.box = settings['vm_box']

        node.vm.provider "virtualbox" do |vb|
          vb.customize ["modifyvm", :id, "--memory", machine['ram']]
          vb.customize ["modifyvm", :id, "--groups", vm_group]
          vb.name = vm_name
        end #vb
          
        node.vm.hostname = vm_name

        node.vm.network "private_network", ip: machine['ip']
        # , netmask: "255.255.0.0"

        # Router machine
        if machine['ip'] == dc['router_ip']

          # node.vm.network "private_network", 
          #   ip: machine['ip'], 
          #   netmask: "255.255.0.0",
          #   # virtualbox__intnet:  vm_internal_network, 
          #   adapter: 2

          # Enable ip forwarding
          node.vm.provision "shell",
            # run: "always",
            inline: "echo 1 > /proc/sys/net/ipv4/ip_forward"

          # Add routes to other dc routers
          settings['datacenters'].each do |otherdc|
            if otherdc != dc
              otherdc['servers'].each do |othermachine|
                # node.vm.provision "shell",
                #   # run: "always",
                #   inline: "ip route del " + otherdc['subnet'] + " via " + otherdc['router_ip'] + " dev enp0s8"
                node.vm.provision "shell",
                  # run: "always",
                  inline: "ip route add " + othermachine['ip'] + " via " + otherdc['router_ip'] # + " dev enp0s8"
              end
            end
          end
          # node.vm.provision "shell",
          #   inline: "ip route del " + dc['subnet'] + " dev enp0s8 "
          # node.vm.provision "shell",
          #   inline: "ip route add " + dc['subnet'] + " dev enp0s8  proto kernel  scope link  src " + machine['ip']

        # Edge machine
        else

          # node.vm.network "private_network", 
          #   ip: machine['ip'], 
          #   netmask: "255.255.255.0",
          #   gw: dc['router_ip'],
          #   # virtualbox__intnet:  vm_internal_network, 
          #   adapter: 2

          # Add routes for the other dcs through the current dc router
          settings['datacenters'].each do |otherdc|
            if otherdc != dc
              otherdc['servers'].each do |othermachine|
                # node.vm.provision "shell",
                #   # run: "always",
                #   inline: "ip route del " + otherdc['subnet'] + " via " + dc['router_ip'] + " dev enp0s8"
                # node.vm.provision "shell",
                #   inline: "ip route del " + otherdc['subnet'] + " dev enp0s8"
                node.vm.provision "shell",
                  # run: "always",
                  inline: "ip route add " + othermachine['ip'] + " via " + dc['router_ip'] #+ " dev enp0s8"
              end
            end
          end
          # node.vm.provision "shell",
          #   inline: "ip route del " + dc['subnet'] + " dev enp0s8 "
          # node.vm.provision "shell",
          #   inline: "ip route add " + dc['subnet'] + " dev enp0s8  proto kernel  scope link  src " + machine['ip']

        end # if

      end # node
    end # machine
  end # dc

  
end
