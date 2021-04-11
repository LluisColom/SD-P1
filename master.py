# -------------------------------------- #										 #
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #
import worker
import multiprocessing as mp
import sys
from xmlrpc.server import SimpleXMLRPCServer
#----------------------------
import requests
from redis import Redis
from rq import Queue

q = Queue(connection=Redis())


WORKER_ID = 1

server = SimpleXMLRPCServer(('localhost',8005), logRequests=True,
	allow_none=True)

def prr(x):
	print("RESULT: {}",x)
# ------------- Server Functions -------------- #
def add_worker():
	#global WORKER_ID
	#wkr = mp.Process(target=worker.start_worker, args=(WORKER_ID,))
	#wkr.start()
	print("Worker afegit.")
	#WORKER_ID += 1

def remove_worker(x):
	#Remove some worker to the cluster.
	pass

def list_worker():
	#List the workers forming the cluster.
	pass

def hello_function(x):
	print (x)
	return x

def submit_task():
	#Submit a task to the cluster.
	result = q.enqueue(hello_function, "jaquemate")

server.register_introspection_functions()
server.register_function(add_worker)
server.register_function(remove_worker)
server.register_function(list_worker)

# ------------ We start the server ------------ #
try:
	server.serve_forever()

except KeyboardInterrupt:
	print("Leaving...")
