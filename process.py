import pickle
import time
import threading
import psutil

class Process:
    def __init__(self, pid, memory_state, cpu_state, resource_allocation):
        self.pid = pid
        self.memory_state = memory_state
        self.cpu_state = cpu_state
        self.resource_allocation = resource_allocation

    def checkpoint(self):
        state = {
            'memory_state': self.memory_state,
            'cpu_state': self.cpu_state,
            'resource_allocation': self.resource_allocation
        }
        with open(f'{self.pid}_checkpoint.pkl', 'wb') as f:
            pickle.dump(state, f)
        print(f"Process {self.pid} checkpointed")

    def restore(self):
        with open(f'{self.pid}_checkpoint.pkl', 'rb') as f:
            state = pickle.load(f)
            self.memory_state = state['memory_state']
            self.cpu_state = state['cpu_state']
            self.resource_allocation = state['resource_allocation']
        print(f"Process {self.pid} restored")

    def get_state(self):
        return {
            'memory_state': self.memory_state,
            'cpu_state': self.cpu_state,
            'resource_allocation': self.resource_allocation
        }

    def update_memory(self):
        process = psutil.Process(self.pid)
        memory_info = process.memory_full_info()
        self.memory_state = memory_info.uss
    def run(self):
        pass


class AdditionProcess:
    def __init__(self, pid, a, b):
        self.pid = pid
        self.a = a
        self.b = b
        self.c = []
        self.stop_event = threading.Event()

    def exec(self):
        for i in range(len(self.a)):
            if self.stop_event.is_set():
                print(f'Process {self.pid} has been stopped.')
                break
            self.c.append(self.a[i] + self.b[i])
            time.sleep(0.5)

    def destination_exec(self, a, b):
        for i in range(len(a)):
            self.c.append(a[i] + b[i])

    def stop(self):
        self.stop_event.set()
        return self.a[len(self.a) - len(self.c):], self.b[len(self.b) - len(self.c):] , self.c