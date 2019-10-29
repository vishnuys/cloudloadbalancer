import os
import requests
from uhashring import HashRing
from traceback import format_exc
from .helper import status_check
from django.shortcuts import render
from clouder.settings import NODE_LIST, NODE_ADDRESS
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class DefaultView(TemplateView):

	def get(self, request):
		return render(request, "index.html")


@method_decorator(csrf_exempt, name='dispatch')
class CreateBucket(TemplateView):

	def post(self, request):
		name = request.POST.get('name')
		hr = HashRing(nodes=NODE_LIST)
		print(hr, type(hr))
		node = hr.get_node(name)
		addr = os.path.join(NODE_ADDRESS[node], 'createbucket/')
		print(node)
		data = {'name': name}
		r = requests.post(addr, data=data)
		print(r.status_code)
		replication_count = r.json['count']+1
		if r.ok and replication_count >= 2:
			result = {
				'status': 'success',
				'node': node,
				'vector_clocks': {}
			}
			return JsonResponse(result)
		elif r.ok and replication_count < 2:
			result = {
				'status': 'failure to write in majority nodes',
				'node': node,
				'vector_clocks': {}
			}
			return JsonResponse(result)
		else:
			return HttpResponse("failed", status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StatusChecker(TemplateView):

	def post(self, request):
		result = status_check()
		return JsonResponse(result)
		