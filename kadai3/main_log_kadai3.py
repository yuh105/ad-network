#!/usr/bin/python
# -*- Coding: utf-8 -*-

from models3 import Queue, Node
import matplotlib.pyplot as plt

def enqueue(queue):
	if log[5] != '40':
		queue.enqueue_tcp()
	elif log[4] == 'ack':
		queue.enqueue_ack()
	elif log[4] == 'tcp':
		queue.enqueue_tcp40()

def dequeue(queue):
	if log[5] != '40':
		queue.dequeue_tcp()
	elif log[4] == 'ack':
		queue.dequeue_ack()
	elif log[4] == 'tcp':
		queue.dequeue_tcp40()

def receive(node):
	if log[5] != '40':
		node.receive_tcp(int(log[5]))
	elif log[4] == 'ack':
		node.receive_ack()
	elif log[4] == 'tcp':
		node.receive_tcp40()

def drop(node):
	if log[5] != '40':
		node.drop_tcp(int(log[5]))
	elif log[4] == 'ack':
		node.drop_ack()
	elif log[4] == 'tcp':
		node.drop_tcp40()

if __name__=='__main__':
	link_a = Queue('link_a')
	link_b = Queue('link_b')
	link_c = Queue('link_c')
	node0 = Node('node0')
	node1 = Node('node1')
	node2 = Node('node2')
	node3 = Node('node3')
	start_time = 0
	end_time = 0

	line = raw_input()
	start_time = line.split()[1]

	# for graph
	x_time = []
	y_drop = []
	y_dropnum = 0

	while line:
		log = line.split()
		end_time = log[1]

		x_time.append(log[1])
		y_drop.append(y_dropnum)

		if log[0] == '+':
			if int(log[2]) + int(log[3]) == 1:
				enqueue(link_a)
			elif int(log[2]) +  int(log[3]) == 3:
				enqueue(link_b)
			elif int(log[2]) +  int(log[3]) == 5:
				enqueue(link_c)

		if log[0] == '-':
			if int(log[2]) + int(log[3]) == 1:
				dequeue(link_a)
			elif int(log[2]) +  int(log[3]) == 3:
				dequeue(link_b)
			elif int(log[2]) +  int(log[3]) == 5:
				dequeue(link_c)

		if log[0] == 'r':
			if log[3] == '0':
				receive(node0)
			elif log[3] == '1':
				receive(node1)
			elif log[3] == '2':
				receive(node2)
			elif log[3] == '3':
				receive(node3)

		if log[0] == 'd':
			y_dropnum += 1
			if log[2] == '0':
				drop(node0)
			elif log[2] == '1':
				drop(node1)
			elif log[2] == '2':
				drop(node2)
			elif log[2] == '3':
				drop(node3)
		try:
			line = raw_input()
		except EOFError:
			break

	through_put = node3.get_packet() * 8 / (float(end_time) - float(start_time))
	print(' - - - - - - - - - - - - - - - - - ')
	print('start_time = ' + start_time)
	print('end_time = ' + end_time)
	print('time = ' + str(float(end_time) - float(start_time)))
	print(' - - - - - - - - - - - - - - - - - ')
	node0.print_result()
	print(' - - - - - - - - - - - - - - - - - ')
	link_a.print_result()
	print(' - - - - - - - - - - - - - - - - - ')
	node1.print_result()
	print(' - - - - - - - - - - - - - - - - - ')
	link_b.print_result()
	print(' - - - - - - - - - - - - - - - - - ')
	node2.print_result()
	print(' - - - - - - - - - - - - - - - - - ')
	link_c.print_result()
	print(' - - - - - - - - - - - - - - - - - ')
	node3.print_result()
	print(' - - - - - - - - - - - - - - - - - ')
	print(node3.name + '.get_packet(bit) = ' + str(node3.get_packet() * 8))

	print('through_put = node3.get_packet (byte) * 8 / (end_time - start_time)')
	print('through_put = ' + str(node3.get_packet()) + ' * 8 / (' + str(end_time) + ' - ' + str(start_time) + ')')
	print('through_put = ' + str(node3.get_packet() * 8) + ' / ' + str(float(end_time) - float(start_time)))
	print('through put = '+ str(through_put) + 'bps')
	print('through put = '+ str(round(through_put/1000, 1)) + 'kbps')
	print('through put = '+ str(round(through_put/1000000, 3))  + 'Mbps')
	print(' - - - - - - - - - - - - - - - - - ')


	plt.plot(x_time, y_drop, label='total drop packets num')
	plt.axis(ymin=0,ymax=y_dropnum+5)
	plt.xlabel('time (sec)')
	plt.ylabel('total drop packets')
	plt.legend(loc='best')

	plt.savefig('d_packet.png')
	# plt.show()
