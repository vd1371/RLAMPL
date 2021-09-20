import threading
import queue

from ._make_request import _make_request

import time

def share_load(ports_of_groups, payloads, groups_of_ids):

	q_out = queue.Queue()
	
	pool = []
	for group, port in ports_of_groups.items():

		payload = payloads[group]
		
		worker = threading.Thread(target = _make_request,
									args = (port, payload, q_out,))

		worker.start()
		pool.append(worker)

	for worker in pool:
		worker.join()

	return q_out