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

		# We execute the task and store the result in the redis DB.
		if (job == "countWords"):
			conn.rpush(id, tasks.countWords(argument))
		elif (job == "wordCount"):
			conn.rpush(id, tasks.wordCount(argument))