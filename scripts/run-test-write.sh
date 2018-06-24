#!/bin/bash

cd /vagrant/performance/nosql-tests/
node benchmark.js neo4j -t singleWriteSync
node benchmark.js neo4j -a 192.168.3.21 -t singleWriteSync
