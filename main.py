from Node import Node
from process import Process
import threading
from process import AdditionProcess



pid = 1
memory_state = {'page1': [1, 3, 4], 'page2': [7, 9, 11], 'page3': [112, 220, 33]}
cpu_state = {'register1': 'value1', 'register2': 'value2'}
resource_allocation = {'resource1': 'allocation1', 'resource2': 'allocation2'}
process = Process(pid, memory_state, cpu_state, resource_allocation)
source_node = Node(node_id=1, host='localhost', port=2000)
destination_node = Node(node_id=2, host='localhost', port=2001)


# def receive_process_thread(node):
#     received_process = node.precopy_receive(target_host='localhost', target_port=2000)
#     print("Received process state:", received_process.get_state())
#
# threading.Thread(target=receive_process_thread, args=(destination_node,)).start()
# print("Starting pre-copy migration")
# source_node.precopy_send(process, target_host='localhost', target_port=2001)

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
addprocess = AdditionProcess(2, a, b)
addprocess.exec()

def receive_process_thread(node):
    node.postcopy_receive(target_host='localhost', target_port=2000)

source_node.postcopy_send(addprocess, target_host='localhost', target_port=2001)

threading.Thread(target=receive_process_thread, args=(destination_node,)).start()
