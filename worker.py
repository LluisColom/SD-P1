# -------------------------------------- #										 #
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #

import sys
from rq import Connection, Worker
from redis import Redis

import tasks

# Hacer bucle while (true):

def start_worker(x):
	redis = Redis()

	with Connection():
		w = Worker(x, connection=redis, name='hola')
		w.work()