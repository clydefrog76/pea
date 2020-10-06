import asyncio

async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        request = (await reader.read(255)).decode('utf8')
        response = str(eval(request)) + '\n'
        writer.write(response.encode('utf8'))
        await writer.drain()
    writer.close()

loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(handle_client, 'localhost', 15555))
loop.run_forever()

# import asyncio

# class EchoProtocol(asyncio.Protocol):
    
#     def connection_made(self, transport):
#         self.transport = transport
    
#     def data_received(self, data):
#         self.transport.write(data)

# async def main(host, port):
#     loop = asyncio.get_running_loop()
#     server = await loop.create_server(EchoProtocol, host, port)
#     await server.serve_forever()

# asyncio.run(main('127.0.0.1', 5000))

# import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('127.0.0.1', 1234))
# s.listen(5)

# while True:
#     # now our endpoint knows about the OTHER endpoint.
#     clientsocket, address = s.accept()
#     print(f"Connection from {address} has been established.")


# import socket

# mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# mySocket.bind(('127.0.0.1', 1024))
# mySocket.listen()

# conn, addr = mySocket.accept()
# with conn:
#     print('Connected by', addr)
#     while True:
#         data = conn.recv(1024)
#         if not data:
#             break
#         conn.sendall(data)        

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind(('127.0.0.1', 1024))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)               


# from multiprocessing.connection import Listener


# listener = Listener(('127.0.0.1', 1024))
# client = listener.accept()
# while 1:
#     try:
#         print(client.recv_bytes())
#     except EOFError:
#         print("Connection closed")
#         #break
#     except OSError:
#         print("Connection closed")
#         #break    