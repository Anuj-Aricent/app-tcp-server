import socket               # Import socket module
import thread
import redis
import os
from urlparse import urlparse

server = socket.socket()
redis_db = redis.StrictRedis(host=str(os.environ['REDIS_SERVICE_HOST']), port=str(os.environ['REDIS_SERVICE_PORT']))
host_server = "0.0.0.0"
port_server = 12341
server.bind((host_server, port_server))
url_addrs_json = eval(redis_db.get('TCP-SERVER-MS'))
url_addrs = str(url_addrs_json["12345"])
client = socket.socket()
addr = urlparse(url_addrs)
host_client = addr.hostname # Get local machine name
port_client = addr.port     # Reserve a port for your service.
client.connect((host_client, port_client))

client_list = []

recvmsg = ""

def recvMsg(s):
    global recvmsg
    while True:
        recvmsg = s.recv(1024)
        if recvmsg:
            print  '<Recieved from main server>>> ' + recvmsg
            for c in client_list:
                c.send(recvmsg)

thread.start_new_thread(recvMsg, (client, ))

server.listen(5)
c, addr = server.accept()
if c not in client_list:
   client_list.append(c)
while True:
   buf= c.recv(1024)
   print buf
   client.send("from aseem:" + buf)

   continue
   c.close()
