from fibonacci import fibonacci
import sys
import asyncio  # 1 - switch from socket to asyncio

async def server(port: int):
    """Deploy a TCP/IP server on 127.0.0.1:{port}"""
    s = await asyncio.start_server(handle, 'localhost', port)  # 2
    async with s:
        await s.serve_forever()

async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):  # 3
    while True:  # Accept multiple requests on the same connection
        data = await reader.readline()  # 4 - conn is now reader
        if not data: 
            addr = writer.get_extra_info("peername")
            port = writer.get_extra_info("sockname")[1]
            print(f"Closed server connection on port {port} from addr {addr}")
            break
        request = int(data.decode())
        response = str(fibonacci(request)).encode() + b'\n'
        writer.write(response)  # 5 - conn is now writer
        await writer.drain()  # 6 drain

if __name__ == "__main__":
    asyncio.run(server(int(sys.argv[1])))
