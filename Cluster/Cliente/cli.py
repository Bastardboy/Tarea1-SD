from flask import Flask, request, render_template  

import grpc
import redis
from random import randint
import proto_message_pb2 as pb2_grpc
import proto_message_pb2_grpc as pb2
#import time

app = Flask(__name__)

r1 = redis.Redis(host="redis1", port=6379, db=0)
r1.config_set('maxmemory', 865200*2)
r1.config_set('maxmemory-policy', 'allkeys-lru')

r2 = redis.Redis(host="redis2", port=6379, db=0)
r2.config_set('maxmemory', 865200*2)
r2.config_set('maxmemory-policy', 'allkeys-lru')

r3 = redis.Redis(host="redis3", port=6379, db=0)
r3.config_set('maxmemory', 865200*2)
r3.config_set('maxmemory-policy', 'allkeys-lru')

r1.flushall()
r2.flushall()
r3.flushall()

redis_global = [r1, r2, r3] #Arreglo que contiene a los 3 redis antriores


class SearchClient(object):

    def __init__(self):
        self.host = 'backend'
        self.server_port = '50051'

        # instantiate a channel
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))
        
        # bind the client and the server
        self.stub = pb2.SearchStub(self.channel)

    def get_url(self, message):
        """
        Client function to call the rpc for GetServerResponse
        """

        message = pb2_grpc.Message(message=message)
        print(f'{message}')
        stub = self.stub.GetServerResponse(message)
        return stub

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET']) #Para definir el tipo de peticion y como hacerla
def search():
    client = SearchClient() 
    search = request.args['search'] #Para obtener los parametro de la url
    cache = list()
    cache.append(r1.get(search))
    cache.append(r2.get(search))
    cache.append(r3.get(search))
    if cache[0] == None and cache[1] == None and cache[2] == None:
        data = client.get_url(message=search)
        rand = randint(0,2)
        location = "Almacenado en redis"+str(rand+1) 
        print(location)
        redis_global[rand].set(search, str(data)) #Alguno de los 3 redis
        
        return render_template('index.html', datos = data, procedencia = "Datos sacados de PostgreSQL ", redis = location)
    
    else:
        for datos in cache:
            if datos != None:
                data = datos.decode("utf-8")
                dicc = dict()
                dicc['Resultado'] = data
                print(dicc)
                return render_template('index.html', datos = data, procedencia = "Datos sacados de Redis")

@app.route('/kk', methods=['GET'])
def kk():
    print(request.args)
    return "holi"

if __name__ == '__main__':
    app.run(debug=True)