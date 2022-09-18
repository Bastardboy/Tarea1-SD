#### CÓDIGO USADO COMO REFERENCIA PARA REALIZAR LA TAREA
## https://github.com/Joacker/Ayu-SD-2022-2/tree/main/Ayu2/python
###

import grpc
from concurrent import futures
import proto_message_pb2 as pb2
import proto_message_pb2_grpc as pb2_grpc
from time import sleep
from routes import querys

class SearchService(pb2_grpc.SearchServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):
        item = []
        response = []
        message = request.message
        result = f'"{message}" '
        
        cursor.execute("SELECT * FROM items;")
        query_res = cursor.fetchall()
        for row in query_res:
            if message in row[1] or message in row[2] or message in row[3] or message in row[4]:	
                item.append(row)
        for i in item:
            result = dict()
            result['id'] = i[0]
            result['title']= i[1]
            result['description'] = i[2]
            result['keywords']= i[3]
            result['url']= i[4]
            response.append(result)
        
        print(pb2.SearchResults(site=response))
        return pb2.SearchResults(site=response)

def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SearchServicer_to_server(SearchService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

    
if __name__ == '__main__':
    conn = querys.init_db()
    cursor = conn.cursor()
    serve()