# -*- mode: ruby -*-
# vi: set ft=ruby :

# Load settings from vagrant.yml file. 
require 'yaml'
settings = YAML.load_file 'vagrant.yml'

# All Vagrant configuration is done below. 
Vagrant.configure("2") do |config|

  # Loop through datacenters
  settings['datacenters'].each do |dc|

    # Loop through servers
    dc['servers'].each do |machine|

      # Variables
      vm_group = '/' + settings['group'] + "/" + dc['name']
      vm_name = settings['group'] + "-" + dc['name'] + '-' + machine['name']

      # Define settings for each node
      config.vm.define vm_name do |node|

        node.vm.box = settings['vm_box']

        node.vm.provider "virtualbox" do |vb|
          vb.customize ["modifyvm", :id, "--memory", machine['ram']]
          vb.customize ["modifyvm", :id, "--cpus", machine['cpus']]
          vb.customize ["modifyvm", :id, "--groups", vm_group]
          vb.name = vm_name
        end #vb
          
        node.vm.hostname = vm_name

        node.vm.network "private_network", ip: machine['ip']

        # Router machine
        if machine['ip'] == dc['router_ip']

          # Enable ip forwarding
          node.vm.provision "shell", run: "always",
            inline: "echo 1 > /proc/sys/net/ipv4/ip_forward"

          # Add routes to other dcs machines through the other dcs routers
          settings['datacenters'].each do |otherdc|
            if otherdc != dc
              otherdc['servers'].each do |othermachine|
                node.vm.provision "shell", run: "always",
                  inline: "ip route add " + othermachine['ip'] + " via " + otherdc['router_ip']
              end
            end
          end

        # Edge machine
        else

          # Add routes to the other dcs machines through the current dc router
          settings['datacenters'].each do |otherdc|
            if otherdc != dc
              otherdc['servers'].each do |othermachine|
                node.vm.provision "shell", run: "always",
                  inline: "ip route add " + othermachine['ip'] + " via " + dc['router_ip']
              end
            end
          end

        end # if
      end # node
    end # machine
  end # dc
end # config
