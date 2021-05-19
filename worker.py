# -------------------------------------- #										 #
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #

import sys
import redis

import tasks

conn = None
id = None

def wordCountMerge(arg):
	pass

def countWordsMerge(elem_number):
	sum = 0
	for i in range(elem_number):
		sum = sum + conn.blpop(id);	#We wait for the other tasks to finish... then we retrieve their result.
	
	return sum

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
		elif (job == "wordCountMerge"):
			conn.rpush(id, wordCountMerge(argument))
		elif (job == "countWordsMerge"):
			conn.rpush(id, countWordsMerge(argument))
