# -------------------------------------- #										 #
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #
import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8005')

print('CLIENT CREAT, afegint worker...')
s.add_worker()
s.submit_task("tasks.write_file","jaquemate")
s.submit_task("tasks.print_function","hola xd")