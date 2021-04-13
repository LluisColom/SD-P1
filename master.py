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

import tasks

#print("REFERENCIA A LA CUA {}".format(q))

WORKER_LIST = {}
WORKER_ID = 1

server = SimpleXMLRPCServer(('localhost',8005), logRequests=True,
	allow_none=True)

def prr(x):
	print("RESULT: {}",x)
# ------------- Server Functions -------------- #
def add_worker():
	wkr = mp.Process(target=worker.start_worker, args=(q,))
	wkr.start()
	print("Worker afegit.")
	WORKER_ID += 1
	WORKER_LIST[WORKER_ID-1] = wkr

def remove_worker(x):
	if (x in WORKER_LIST):
		Process = WORKER_LIST(x).terminate()
		del WORKER_LIST[x]

def list_worker():
	# Si falla pasarlo a string
	return WORKER_LIST

def submit_task(x, y):
	result = q.enqueue(x, y)

server.register_introspection_functions()
server.register_function(add_worker)
server.register_function(submit_task)
server.register_function(remove_worker)
server.register_function(list_worker)

# ------------ We start the server ------------ #
try:
	server.serve_forever()

except KeyboardInterrupt:
	print("Leaving...")
