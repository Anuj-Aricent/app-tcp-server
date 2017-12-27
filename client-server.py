import socket               # Import socket module
import thread
import redis

redis_db = redis.StrictRedis(host=str(os.environ['REDIS_SERVICE_HOST']), port=str(os.environ['REDIS_SERVICE_PORT']))
server = socket.socket()
host_server = "0.0.0.0"
port_server = 12341
server.bind((host_server, port_server))

client = socket.socket()
host_client =  eval(redis_db.get('TCP_HOST'))
port_client = eval(redis_db.get('TCP_PORT'))
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
while True:
   c, addr = server.accept()
   if c not in client_list:
       client_list.append(c)
   buf= c.recv(1024)
   print buf
   client.send("from aseem:" + buf)
   
   continue
   c.close()
