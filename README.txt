
El codi cal executar-lo a Linux.

Primer executar el master.py i a continuació, client.py.


Al client.py hi ha la interfície on pots gestionar el cluster i enviar tasques.


La comunicació client-servidor es realitza mitjançant comunicació directa,
amb XML-RPC. La comunicació servidor-treballador es realitza de forma indirecta,
a través de Redis.

Per a que el codi funcioni cal tenir el dimoni redis-server obert.

Els resultats es mostren de forma assincrona a l'usuari, de forma que aquest
pot anar realitzant de forma seguida varies accions sense tenir el client
bloquejat esperant a que una tasca finalitzi.


