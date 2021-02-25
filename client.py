# -------------------------------------- #										 #
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #
import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8005')

print('CLIENT CREAT, afegint worker...')
s.add_worker()