# -------------------------------------- #										 #
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #

import sys
import redis

import tasks

def start_worker(x):
	conn = redis.StrictRedis(host='localhost', port=6379, db=0)
	while (True):
		job, id = conn.blpop('task_queue')
		argument = conn.blpop('arg_queue')

		if (job == tasks.print_function):
			conn.rpush(id, tasks.print_function(argument))
		else:
			conn.rpush(id, tasks.write_file(argument))