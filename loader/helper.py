import os
import requests
from traceback import format_exc
from clouder.settings import NODE_LIST, NODE_ADDRESS

def status_check():
	result = {}
	for i in NODE_LIST:
		try:
			addr = os.path.join(NODE_ADDRESS[i], 'status/')
			r = requests.get(addr)
			if r.ok:
				result[i] = 'Live'
			else:
				result[i] = 'Down'

		except Exception:
			print(format_exc())
			result[i] = 'Down'
	return result