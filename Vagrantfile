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
      vm_group = '/' + settings['vm_group'] + "/" + dc['name']
      vm_name = settings['vm_group'] + "-" + dc['name'] + '-' + machine['name']

      # Define settings for each node
      config.vm.define vm_name do |node|

        node.vm.box = settings['vm_box']

        node.vm.provider "virtualbox" do |vb|
          vb.customize ["modifyvm", :id, "--memory", machine['ram']]
          vb.customize ["modifyvm", :id, "--cpus", machine['cpus']]
          vb.customize ["modifyvm", :id, "--groups", vm_group]
          vb.name = vm_name
          # vb.linked_clone = true
        end #vb
          
        node.vm.hostname = vm_name

        node.vm.network "private_network", ip: machine['ip']

        # Router machine
        if machine['ip'] == dc['router_ip']

          # Enable ip forwarding
          node.vm.provision "shell", 
            run: "always",
            inline: "echo 1 > /proc/sys/net/ipv4/ip_forward"

          # Add routes to other dcs machines through the other dcs routers
          settings['datacenters'].each do |otherdc|
            if otherdc != dc
              otherdc['servers'].each do |othermachine|
                if othermachine['ip'] != otherdc['router_ip']
                  node.vm.provision "shell", 
                    run: "always",
                    inline: "ip route add " + othermachine['ip'] + " via " + otherdc['router_ip']
                end
              end
            end
          end

        # Edge machine
        else

          # Add routes to the other dcs machines through the current dc router
          settings['datacenters'].each do |otherdc|
            if otherdc != dc
              otherdc['servers'].each do |othermachine|
                node.vm.provision "shell", 
                  run: "always",
                  inline: "ip route add " + othermachine['ip'] + " via " + dc['router_ip']
              end
            end
          end

        end # if

        # Ansible provisioning

        # Disable the new default behavior introduced in Vagrant 1.7, to
        # ensure that all Vagrant machines will use the same SSH key pair.
        # See https://github.com/mitchellh/vagrant/issues/5005
        node.ssh.insert_key = false

        # Determine neo4j_initial_hosts 
        node_ip = machine['ip']
        node_id = machine['id']
        neo4j_dbms_mode = machine['neo4j_dbms_mode']
        neo4j_server_groups = machine['neo4j_server_groups']
        neo4j_database = dc['neo4j_database']
        initial_node_ip = settings['neo4j_initial_node']
        neo4j_initial_discovery_members = settings['neo4j_initial_discovery_members']
        neo4j_heap_initial_size = settings['neo4j_heap_initial_size']
        neo4j_heap_max_size = settings['neo4j_heap_max_size']
        neo4j_pagecache_size = settings['neo4j_pagecache_size']
        neo4j_minimum_core_cluster_size_at_formation = settings['neo4j_minimum_core_cluster_size_at_formation']
        neo4j_minimum_core_cluster_size_at_runtime = settings['neo4j_minimum_core_cluster_size_at_runtime']
        host_coordination_port = settings['neo4j_host_coordination_port'].to_s
        # neo4j_initial_hosts = initial_node_ip + ":" + host_coordination_port
        neo4j_initial_hosts = settings['neo4j_initial_hosts']

        # Call Ansible also passing it values needed for configuration
        node.vm.provision "ansible_local" do |ansible|
          ansible.verbose = "v"
          ansible.playbook = "playbook.yml"
          ansible.extra_vars = {
            node_ip_address: node_ip,
            neo4j_server_id: node_id,
            neo4j_initial_hosts: neo4j_initial_hosts,
            neo4j_initial_discovery_members: neo4j_initial_discovery_members,
            neo4j_heap_initial_size: neo4j_heap_initial_size,
            neo4j_heap_max_size: neo4j_heap_max_size,
            neo4j_pagecache_size: neo4j_pagecache_size,
            neo4j_minimum_core_cluster_size_at_formation: neo4j_minimum_core_cluster_size_at_formation,
            neo4j_minimum_core_cluster_size_at_runtime: neo4j_minimum_core_cluster_size_at_runtime,
            neo4j_dbms_mode: neo4j_dbms_mode,
            neo4j_server_groups: neo4j_server_groups,
            neo4j_database: neo4j_database
        }
        end

        node.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

        node.vm.provision "shell", 
          run: "always",
          inline: "service neo4j restart"

        delay_script = "scripts/delay-" + dc['name'] + ".sh"
        node.vm.provision "shell", 
          run: "always",
          path: delay_script

      end # node
    end # machine
  end # dc
end # config
