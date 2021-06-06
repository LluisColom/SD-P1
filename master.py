# -------------------------------------- #										 #
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #
import worker
import multiprocessing as mp
from xmlrpc.server import SimpleXMLRPCServer
import redis

WORKER_LIST = {}
WORKER_ID = 0
JOB_ID = 1

# ---------------------------- Connex Establishment ----------------------------- #
print ("Starting server...")
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
server = SimpleXMLRPCServer(('localhost',8005), allow_none=True)
server.register_introspection_functions()

# ------------------------------ Server Functions ------------------------------- #
def add_worker():
	global WORKER_ID		
	global WORKER_LIST
	wkr = mp.Process(target=worker.start_worker, args=(WORKER_ID,))
	wkr.start()

	id = "W-"+str(WORKER_ID)
	WORKER_LIST[id] = wkr
	WORKER_ID += 1
	return "Worker with ID {} succesfully added.".format(id)

def remove_worker(x):
	global WORKER_LIST
	log = ""
	 
	for id in x.split(" "):
		
		if id in WORKER_LIST.keys():
			WORKER_LIST[id].terminate()
			del WORKER_LIST[id]
			log = log + "Worker with ID {} removed.".format(id) + "\n"
		else:
			log = log + "No worker with ID {} found.".format(id) + "\n"

	return log

def list_worker():
	global WORKER_LIST	
	x = ""
	for wkr in WORKER_LIST.keys():
		x = x + wkr + "\n"
	
	if len(x) == 0:
		return "No active workers."
	else:
		return x # String con los pid de los WORKERS activos

def submit_task(x,y):
	global JOB_ID
	split_args = y.split(' ')
	# Guardamos en 'task_queue' las tareas a realizar.
	if(len(split_args) > 1):
		for arg in split_args:
			redisClient.rpush('task_queue', x, JOB_ID)
			redisClient.rpush('arg_queue', "http://localhost:8000/"+arg)
		# Harmonize the results.
		redisClient.rpush('task_queue', x+str("Merge"), JOB_ID)
		num_elem = len (split_args)
		redisClient.rpush('arg_queue', num_elem)
	else:
		redisClient.rpush('task_queue', x, JOB_ID)
		redisClient.rpush('arg_queue', "http://localhost:8000/"+y)
	
	JOB_ID = JOB_ID + 1
	return JOB_ID-1

def check_result(x):
	return redisClient.lpop(x)


server.register_function(add_worker)
server.register_function(remove_worker)
server.register_function(list_worker)
server.register_function(submit_task)
server.register_function(check_result)


#---------------------------------------- MAIN ----------------------------------------


# ------------ We start the server ------------ #
print("Ready to serve queries...")

try:
	server.serve_forever()

except KeyboardInterrupt:
	print("Shutting down...")