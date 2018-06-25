#!/bin/bash

cat /vagrant/hosts.out | while read line
do
   last=${line##* }
   ping -c 3 $last
done

