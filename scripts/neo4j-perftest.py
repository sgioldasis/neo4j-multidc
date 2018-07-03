#!/usr/bin/env python

from neo4j.v1 import GraphDatabase
from datetime import datetime
import argparse
import time
    
parser = argparse.ArgumentParser()
parser.add_argument("--server", help="Server to connect", default="localhost")
parser.add_argument("--protocol", help="Protocol to use", default="bolt")
parser.add_argument("--num_recs", help="Number of records to write", type=int, default=1000)
parser.add_argument("--commit_every", help="Number of records after which to commit", type=int, default=100)
args = parser.parse_args()

driver = GraphDatabase.driver(args.protocol+"://"+args.server+":7687")

def create_person(driver, name):
    with driver.session() as session:
        tx = session.begin_transaction()
        node_id = create_person_node(tx)
        set_person_name(tx, node_id, name)
        tx.commit()

def create_person_node(tx):
    return tx.run("CREATE (a:Person)"
                  "RETURN id(a)").single().value()

def set_person_name(tx, node_id, name):
    tx.run("MATCH (a:Person) WHERE id(a) = $id "
           "SET a.name = $name", id=node_id, name=name)

# Write test
startWrite = time.time()
with driver.session() as session:
    tx = session.begin_transaction()
    uncommited = True
    for id in range(1, args.num_recs+1):
        name = "User" + str(id)
        node_id = create_person_node(tx)
        # set_person_name(tx, node_id, name)
        uncommited = True
        if id%args.commit_every == 0:
            print("Committing [{recs}]".format(recs=id))
            tx.commit()
            uncommited = False
            if id < args.num_recs:
                tx = session.begin_transaction()
                uncommited = True
    
    if uncommited:
        print('Committing [' + str(id) + ']')
        tx.commit()
elapsedWrite = time.time() - startWrite


# Read test
num_read = 0
def read_all_nodes(tx):
    global num_read
    for record in tx.run("MATCH (n) RETURN n"):
        # print record['n'].id
        num_read = num_read + 1

startRead = time.time()
with driver.session() as session:
    session.read_transaction(read_all_nodes)    
elapsedRead = time.time() - startRead



# Results
print
print("ARGUMENTS:")
print("   server       = {server}".format(server=args.server))
print("   protocol     = {protocol}".format(protocol=args.protocol))
print("   num_recs     = {num_recs}".format(num_recs=args.num_recs))
print("   commit_every = {commit_every}".format(commit_every=args.commit_every))

print
print("WRITE [{num_recs} rows]:\nElapsed: {elapsed}, RPS: {rps}" 
    .format(num_recs=args.num_recs,commit_every=args.commit_every,elapsed=elapsedWrite,
    rps=round(args.num_recs/elapsedWrite,1)))

print
print("READ [{num_read} rows]:\nElapsed: {elapsed}, RPS: {rps}" 
    .format(num_read=num_read,elapsed=elapsedRead,
    rps=round(num_read/float(elapsedRead),1)))


print
