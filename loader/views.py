import os
import requests
from traceback import format_exc
from django.shortcuts import render
from clouder.settings import NODE_LIST
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
		return HttpResponse("Request Recieved")


@method_decorator(csrf_exempt, name='dispatch')
class StatusChecker(TemplateView):

	def post(self, request):
		result = {}
		for i in NODE_LIST:
			try:
				addr = os.path.join(i['address'], 'status/')
				r = requests.get(addr)
				if r.ok:
					result[i['name']] = 'Live'
				else:
					result[i['name']] = 'Down'

			except Exception:
				print(format_exc())
				result[i['name']] = 'Down'
		return JsonResponse(result)
		