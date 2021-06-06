# -------------------------------------- #										 #
# Programador: David Nava Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #
import json
import redis
import tasks

conn = None
id = None

# ------------------------------ MERGING FUNCTIONS ------------------------------

def wordCountMerge():
	global id
	global conn
	result = json.loads("{"+str(conn.blpop(id)).split("{")[1].split("}")[0]+"}")
	
	while (conn.llen(id) != 0):
		#result.update(json.loads("{"+str(conn.blpop(id)).split("{")[1].split("}")[0]+"}"))
		result = {**result, **json.loads("{"+str(conn.blpop(id)).split("{")[1].split("}")[0]+"}")}

	return str(result)


def countWordsMerge():
	global id
	global conn
	sum = 0
	while (conn.llen(id) != 0):
		sum = sum + int(conn.lpop(id));	#We wait for the other tasks to finish... then we retrieve their result.
	
	return sum


# -------------------------------------- MAIN --------------------------------------

def start_worker(x):
	global id
	global conn
	conn = redis.StrictRedis(host='localhost', port=6379, db=0)

	while (True):
		job = str(conn.blpop('task_queue')).split("'")[3]
		id = str(conn.lpop('task_queue')).split("'")[1]
		argument = str(conn.blpop('arg_queue')).split("'")[3]

		# We execute the task and store the result in the redis DB.
		if (job == "countWords"):
			conn.rpush(id, tasks.countWords(argument))
		elif (job == "wordCount"):
			conn.rpush(id, tasks.wordCount(argument))
		elif (job == "wordCountMerge"):
			conn.rpush(id, wordCountMerge())
		elif (job == "countWordsMerge"):
			conn.rpush(id, countWordsMerge())
