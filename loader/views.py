import os
import requests
from uhashring import HashRing
from traceback import format_exc
from .helper import status_check
from django.shortcuts import render
from IPython import embed
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from clouder.settings import NODE_LIST, NODE_ADDRESS, REPLICATION_FACTOR
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, HttpResponseBadRequest


# Create your views here.
class DefaultView(TemplateView):

	def get(self, request):
		return render(request, "index.html")


@method_decorator(csrf_exempt, name='dispatch')
class CreateBucket(TemplateView):

	def post(self, request):
		name = request.POST.get('name')
		node_status = status_check()
		alive_nodes = [x for x in NODE_LIST if node_status[x]=='Live']
		hr = HashRing(nodes=alive_nodes)
		print(hr, type(hr))
		node = hr.get_node(name)
		addr = os.path.join(NODE_ADDRESS[node], 'createbucket/')
		print(node)
		data = {'name': name}
		r = requests.post(addr, data=data)
		print(r.status_code)
		replication_count = r.json()['count']
		node_result = r.json()['result']
		print('result=%s count=%d' % (node_result, replication_count))
		if r.ok and replication_count >= REPLICATION_FACTOR:
			result = {
				'status': 'success',
				'node': node,
				'vector_clocks': {}
			}
			return JsonResponse(result)
		elif r.ok and replication_count == 0:
			return HttpResponseBadRequest(node_result)
		elif r.ok and replication_count < REPLICATION_FACTOR:
			result = {
				'status': 'failure to write in majority nodes',
				'node': node,
				'vector_clocks': {}
			}
			return JsonResponse(result)
		else:
			return HttpResponseServerError("failed")


@method_decorator(csrf_exempt, name='dispatch')
class DeleteBucket(TemplateView):

	def post(self, request):
		name = request.POST.get('name')
		node_status = status_check()
		alive_nodes = [x for x in NODE_LIST if node_status[x]=='Live']
		hr = HashRing(nodes=alive_nodes)
		print(hr, type(hr))
		node = hr.get_node(name)
		addr = os.path.join(NODE_ADDRESS[node], 'deletebucket/')
		print(node)
		data = {'name': name}
		r = requests.post(addr, data=data)
		print(r.status_code)
		replication_count = r.json()['count']
		node_result = r.json()['result']
		print('result=%s count=%d' % (node_result, replication_count))
		if r.ok and replication_count >= REPLICATION_FACTOR:
			result = {
				'status': 'success',
				'node': node,
				'vector_clocks': {}
			}
			return JsonResponse(result)
		elif r.ok and replication_count == 0:
			return HttpResponseBadRequest(node_result)
		elif r.ok and replication_count < REPLICATION_FACTOR:
			result = {
				'status': 'failure to write in majority nodes',
				'node': node,
				'vector_clocks': {}
			}
			return JsonResponse(result)
		else:
			return HttpResponseServerError("failed")


@method_decorator(csrf_exempt, name='dispatch')
class StatusChecker(TemplateView):

	def post(self, request):
		result = status_check()
		return JsonResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class CreateFile(TemplateView):

	def post(self, request):
		try:
			file = request.FILES['file']
			name = request.POST['name']
			bucket = request.POST['bucket']
		except MultiValueDictKeyError:
			return HttpResponseBadRequest('Please enter valid name, bucket and select a valid file to upload')
		if name == '' or bucket == '':
			return HttpResponseBadRequest('Please enter valid name, bucket and select a valid file to upload')

		node_status = status_check()
		alive_nodes = [x for x in NODE_LIST if node_status[x]=='Live']
		hr = HashRing(nodes=alive_nodes)
		print(hr, type(hr))
		node = hr.get_node(file.name)
		addr = os.path.join(NODE_ADDRESS[node], 'createfile/')
		print(node)
		data = {'name': file.name, 'bucket': bucket}
		filedata = {'file': file}
		r = requests.post(addr, data=data, files=filedata)
		print(r.status_code)
		replication_count = r.json()['count']
		node_result = r.json()['result']
		print('result=%s count=%d' % (node_result, replication_count))
		if r.ok and replication_count >= REPLICATION_FACTOR:
			result = {
				'status': 'success',
				'node': node,
				'vector_clocks': {}
			}
			return JsonResponse(result)
		elif r.ok and replication_count == 0:
			return HttpResponseBadRequest(node_result)
		elif r.ok and replication_count < REPLICATION_FACTOR:
			result = {
				'status': 'failure to write in majority nodes',
				'node': node,
				'vector_clocks': {}
			}
			return JsonResponse(result)
		else:
			return HttpResponseServerError("failed")
