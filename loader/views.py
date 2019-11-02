import os
import requests
from .helper import status_check, node_to_contact, handle_result
from django.shortcuts import render
from IPython import embed
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from clouder.settings import NODE_ADDRESS
from django.http import JsonResponse, HttpResponseServerError, HttpResponseBadRequest


# Create your views here.
class DefaultView(TemplateView):

    def get(self, request):
        return render(request, "index.html")


@method_decorator(csrf_exempt, name='dispatch')
class CreateBucket(TemplateView):

    def post(self, request):
        name = request.POST.get('name')
        if name == '':
            return HttpResponseBadRequest('Please enter valid bucket name')
        node = node_to_contact(name)
        addr = os.path.join(NODE_ADDRESS[node], 'createbucket/')
        data = {'name': name}
        r = requests.post(addr, data=data)
        result, response = handle_result(r, node)
        if response == 'SUCCESS':
            return JsonResponse(result)
        elif response == 'BAD_REQUEST':
            return HttpResponseBadRequest(result)
        elif response == 'SERVER_ERROR':
            return HttpResponseServerError(result)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteBucket(TemplateView):

    def post(self, request):
        name = request.POST.get('name')
        if name == '':
            return HttpResponseBadRequest('Please enter valid bucket name')
        node = node_to_contact(name)
        data = {'name': name}
        addr = os.path.join(NODE_ADDRESS[node], 'deletebucket/')
        r = requests.post(addr, data=data)
        result, response = handle_result(r, node)
        if response == 'SUCCESS':
            return JsonResponse(result)
        elif response == 'BAD_REQUEST':
            return HttpResponseBadRequest(result)
        elif response == 'SERVER_ERROR':
            return HttpResponseServerError(result)


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
            name = request.POST['name'].strip()
            bucket = request.POST['bucket'].strip()
        except MultiValueDictKeyError:
            return HttpResponseBadRequest('Please enter valid name, bucket and select a valid file to upload')
        if name == '' or bucket == '':
            return HttpResponseBadRequest('Please enter valid name, bucket and select a valid file to upload')

        node = node_to_contact(name)
        data = {'name': name, 'bucket': bucket}
        addr = os.path.join(NODE_ADDRESS[node], 'createfile/')
        filedata = {'file': file}
        r = requests.post(addr, data=data, files=filedata)
        result, response = handle_result(r, node)
        if response == 'SUCCESS':
            return JsonResponse(result)
        elif response == 'BAD_REQUEST':
            return HttpResponseBadRequest(result)
        elif response == 'SERVER_ERROR':
            return HttpResponseServerError(result)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFile(TemplateView):

    def post(self, request):
        try:
            name = request.POST['name'].strip()
            bucket = request.POST['bucket'].strip()
        except MultiValueDictKeyError:
            return HttpResponseBadRequest('Please enter valid name, bucket and select a valid file to upload')
        if name == '' or bucket == '':
            return HttpResponseBadRequest('Please enter valid name, bucket and select a valid file to upload')

        node = node_to_contact(name)
        data = {'name': name, 'bucket': bucket}
        addr = os.path.join(NODE_ADDRESS[node], 'deletefile/')
        r = requests.post(addr, data=data)
        result, response = handle_result(r, node)
        if response == 'SUCCESS':
            return JsonResponse(result)
        elif response == 'BAD_REQUEST':
            return HttpResponseBadRequest(result)
        elif response == 'SERVER_ERROR':
            return HttpResponseServerError(result)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateFile(TemplateView):

    def post(self, request):
        try:
            name = request.POST['name'].strip()
            bucket = request.POST['bucket'].strip()
            file = request.FILES['file']
        except MultiValueDictKeyError:
            return HttpResponseBadRequest('Please enter valid name, bucket and select a valid file to upload')
        if name == '' or bucket == '':
            return HttpResponseBadRequest('Please enter valid name, bucket and select a valid file to upload')

        node = node_to_contact(name)
        data = {'name': name, 'bucket': bucket}
        filedata = {'file': file}
        addr = os.path.join(NODE_ADDRESS[node], 'updatefile/')
        r = requests.post(addr, data=data, files=filedata)
        result, response = handle_result(r)
        if response == 'SUCCESS':
            return JsonResponse(result)
        elif response == 'BAD_REQUEST':
            return HttpResponseBadRequest(result)
        elif response == 'SERVER_ERROR':
            return HttpResponseServerError(result)
