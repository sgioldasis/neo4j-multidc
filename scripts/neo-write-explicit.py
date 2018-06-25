#!/usr/bin/env python

from neo4j.v1 import GraphDatabase
from datetime import datetime
import argparse
    
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


startTime = datetime.now()
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

elapsed = datetime.now() - startTime
print
print("Elapsed time [Explicitly wrote {num_recs}, commit every {commit_every}] : {elapsed}" 
    .format(num_recs=args.num_recs,commit_every=args.commit_every,elapsed=elapsed))
print
    