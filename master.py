# -------------------------------------- #										 #
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #
import worker
import multiprocessing as mp
import sys
from xmlrpc.server import SimpleXMLRPCServer
import json
#----------------------------
import requests
import redis
from rq import Queue

import tasks

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

WORKER_LIST = []
WORKER_ID = 0
JOB_ID = 0

server = SimpleXMLRPCServer(('localhost',8005), logRequests=True, allow_none=True)

# ------------- Server Functions -------------- #

def add_worker():
	global WORKER_ID		
	global WORKER_LIST
	wkr = mp.Process(target=worker.start_worker, args=(WORKER_ID,))
	wkr.start()
	WORKER_LIST[WORKER_ID] = wkr
	WORKER_ID += 1
	print("Worker afegit amb pid = ", wkr.pid, ".")

def remove_worker(x):
	global WORKER_LIST

	for proc in WORKER_LIST:
		if (proc.pid in x):
			WORKER_LIST.remove(proc)
			proc.terminate()
			print("Worker amb pid ", proc.pid ," esborrat.")

def list_worker():
	global WORKER_LIST	
	x = ""
	for proc in WORKER_LIST:
		x += proc.pid + "\n"
	return x # String con los pid de los WORKERS activos

def submit_task(x,y):
	global JOB_ID
	
	y.split(';')
	# Guardamos en 'task_queue' las tareas a realizar.
	if(len(y) > 1):
		for arg in y:
			redisClient.rpush('task_queue', x, JOB_ID)
			redisClient.rpush('arg_queue', arg)
		# Harmonice the results.
	else:
		redisClient.rpush('task_queue', x, JOB_ID)
		redisClient.rpush('arg_queue', y)
	JOB_ID = JOB_ID + 1



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