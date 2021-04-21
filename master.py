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

import tasks

redisClient = redis.StrictRedis(host='localhost',

                                port=6379,

                                db=0)

WORKER_LIST = {}
WORKER_ID = 0

server = SimpleXMLRPCServer(('localhost',8005), logRequests=True,
	allow_none=True)

# ------------- Server Functions -------------- #

def add_worker():
	global WORKER_ID		
	global WORKER_LIST
	wkr = Process(target=worker.start_worker, args=(WORKER_ID,))
	wkr.start()
	WORKER_LIST[WORKER_ID] = wkr
	WORKER_ID += 1
	print("Worker afegit.")

def remove_worker(x):
	global WORKER_LIST
	for proc in WORKER_LIST:
		if (proc.pid = x):
			proc.terminate()
			del WORKER_LIST[proc]
			print("Worker esborrat.")

def list_worker():
	global WORKER_LIST	
	x = ""
	for proc in WORKER_LIST:
		x += proc.pid + ", "
	return x # String con los pid de los WORKERS activos

def submit_task(x, z):
	redisClient.rpush('Tasks', x, len(z)) # Guardamos en 'Tasks' la tarea a realizar y cuantos arguemtentos tiene
	for arg in z:
		redisClient.rpush('Arguments', z) # Guardamos los argumentos en 'Arguments'

def submit_some_tasks(x): # Formato de x = Tarea1, Num_argumentos, Argumento1, Argumento2, ..., Tarea2, Num_argumentos, Argumento1, Argumento2, ...
	x.split(',')
	if (len(x) > 0):
		index = 0
		while (index != len(x)):	
			n_arg = x[index+1]
			redisClient.rpush('Tasks', x[index], n_arg) # Guardamos en 'Tasks' la tarea a realizar y cuantos arguemtentos tiene
			index = index + 2
			for i in range (n_arg):
				arg = x[index]
				redisClient.rpush('Arguments', arg) # Guardamos los argumentos en 'Arguments'
				index = index + 1

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