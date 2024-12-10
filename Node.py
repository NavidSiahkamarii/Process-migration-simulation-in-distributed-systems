import socket
import pickle
import time
from process import Process
from process import AdditionProcess
class Node:
    def __init__(self, node_id, host, port):
        self.node_id = node_id
        self.host = host
        self.port = port

    def precopy_send(self, process, target_host, target_port):
        print(f"Starting precopy send of process {process.pid}")
        self.send_data('cpu', process, target_host, target_port)
        self.send_data('resource', process, target_host, target_port)
        self.send_data('memory', process, target_host, target_port)
        process.stop()
        print("precopy send of process", process.pid, "finished")


    def precopy_receive(self, target_host, target_port):

        cpu_state = self.receive_data(target_host, target_port)
        recource_state = self.receive_data(target_host, target_port)


        pages = self.receive_data(target_host, target_port)

        while True:
            page = self.receive_data(target_host, target_port)
            if not page:
                break
            pages[page.first] = page.second

        process = Process(5, pages, cpu_state, recource_state)
        process.run()

    def postcopy_send(self, addprocess, target_host, target_port):
        print(f"Starting postcopy of process {addprocess.pid}")
        a, b, c = addprocess.stop()
        while a:
            a = a[5:]
            b = b[5:]
            self.send([a[:5], b[0:5]], target_host, target_port)
            message = self.receive_data(target_host, target_port)
            while message != 'send':
                time.sleep(0.5)

        self.send(c, target_host, target_port)
        print(f"Postcopy of process {addprocess.pid} completed")


    def postcopy_receive(self, target_host, target_port):

        addprocess = AdditionProcess(4, [], [])
        while True:
            a, b = self.receive_data(target_host, target_port)
            if not a:
                break
            addprocess.destination_exec(a, b)
            self.send('send', target_host, target_port)
        c = addprocess.c
        previous_c = self.receive_data(target_host, target_port)
        previous_c.append(c)
        return c

    def send_data(self, which, process, target_host, target_port):
        if which == 'memory':
            temp = process.memory_state
            self.send(process.memory_state, target_host, target_port)
            process.update_memory()

            page_size = 1024
            pages = [temp[i:i + page_size] for i in range(0, len(temp), page_size)]
            updated_pages = [process.memory_state[i:i + page_size] for i in range(0, len(process.memory_state), page_size)]
            while pages != updated_pages:
                for idx, page in enumerate(pages):
                    if pages[idx] != updated_pages[idx]:
                        process.send({f"page_{idx}": page}, target_host, target_port)
                time.sleep(1)

        elif which == 'cpu':
            self.send(process.cpu_state, target_host, target_port)

        else:
            self.send(process.resource_allocation, target_host, target_port)

    def receive_data(self, target_host, target_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_host, target_port))
            data = s.recv(1024)
            s.close()
        return pickle.loads(data)

    def send(self, data, target_host, target_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            data = pickle.dumps(data)
            s.connect((target_host, target_port))
            s.sendall(data)
            s.close()
