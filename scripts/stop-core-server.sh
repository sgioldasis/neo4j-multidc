#!/bin/bash

sudo service neo4j stop
sudo neo4j-admin unbind
sudo rm -rf /var/lib/neo4j/data/databases/graph.db
