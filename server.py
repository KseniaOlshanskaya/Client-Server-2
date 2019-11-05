import asyncio


class Server:
    def __init__(self):
        self.metrics = {}

    def get(self, data):
        if len(data[4:].split()) > 1 or len(data[4:].split()) == 0:
            return 'error\nwrong command\n\n'
        if self.metrics == dict():
            return "No data in dict yet"
        if data[:5] == "get *":
            data_to_return = "ok\n"
            for metric in self.metrics:
                for cortege in self.metrics.get(metric):
                    data_to_return += metric + " " + cortege[0] \
                                          + " " + cortege[1] + "\n"
        else:
            metric_name = data[4:].strip()
            if metric_name not in self.metrics:
                return "ok\n\n"
            data_to_return = "ok\n"
            for metric in self.metrics:
                if metric == metric_name:
                    for cortege in self.metrics.get(metric):
                        data_to_return += metric + " " + cortege[0] \
                                        + " " + cortege[1] + "\n"
                else:
                    pass
        data_to_return += "\n"
        print(data_to_return)
        return data_to_return

    def put(self, data):
        data = data[4:].split()
        if data[0] not in self.metrics:
            self.metrics[data[0]] = [(data[1], data[2])]
            return "ok\n\n"
        else:
            for metric in self.metrics:
                if data[0] == metric:
                    if (data[1], data[2]) in self.metrics[metric]:

                        return "ok\n\n"

                    else:
                        self.metrics[metric].append((data[1], data[2]))

                        return "ok\n\n"


class ServerClientProtocol(asyncio.Protocol):

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport

    def data_received(self, data):
        self.process_data(data.decode())

    def process_data(self, data):
        if data[:3] == "put":
            response = server.put(data)
        elif data[:3] == "get":
            response = server.get(data)
        else:
            response = 'error\nwrong command\n\n'
        self.transport.write(response.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    server_coroutine = loop.create_server(ServerClientProtocol, host, int(port))
    server = loop.run_until_complete(server_coroutine)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


server = Server()
run_server("127.0.0.1", 8888)
