import os
import requests
import mimetypes
from uuid import uuid4
from IPython import embed
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from clouder.settings import NODE_ADDRESS, ARCHIVE_DIR
from django.utils.datastructures import MultiValueDictKeyError
from .helper import status_check, node_to_contact, handle_result
from django.http import HttpResponse, JsonResponse, HttpResponseServerError, \
    HttpResponseBadRequest, HttpResponseNotFound


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
        result, response = handle_result(r, node)
        if response == 'SUCCESS':
            return JsonResponse(result)
        elif response == 'BAD_REQUEST':
            return HttpResponseBadRequest(result)
        elif response == 'SERVER_ERROR':
            return HttpResponseServerError(result)


@method_decorator(csrf_exempt, name='dispatch')
class ReadFile(TemplateView):

    def post(self, request):
        try:
            name = request.POST['name'].strip()
            bucket = request.POST['bucket'].strip()
        except MultiValueDictKeyError:
            return HttpResponseBadRequest('Please enter valid name and bucket')
        if name == '' or bucket == '':
            return HttpResponseBadRequest('Please enter valid name and bucket')

        data = {'name': name, 'bucket': bucket}
        vectors = {}
        vectorlist = []
        for node in NODE_ADDRESS:
            addr = os.path.join(NODE_ADDRESS[node], 'getvector/')
            r = requests.post(addr, data=data)
            nodevector = r.json()['vector']
            vectors[node] = nodevector
            vectorlist.append(nodevector)
        if len(set(vectorlist)) == 1:
            print('All nodes are consistent')
            node = node_to_contact(name)
            addr = os.path.join(NODE_ADDRESS[node], 'file', bucket, name)
            r = requests.get(addr)
            fpath = os.path.join(ARCHIVE_DIR, name)
            with open(fpath, 'wb') as fp:
                fp.write(r.content)
            result = '/file/%s' % name
            return HttpResponse(result)


@method_decorator(csrf_exempt, name='dispatch')
class FileDownload(TemplateView):

    def get(self, request, name):
        print(name)
        filepath = os.path.join(ARCHIVE_DIR, name)
        if not os.path.exists(filepath):
            print('NOT FOUND')
            return HttpResponseNotFound('File not found')
        mimetype = mimetypes.MimeTypes().guess_type(filepath)[0]
        response = HttpResponse()
        response['X-Sendfile'] = filepath
        response['Content-Type'] = mimetype
        response['Content-Disposition'] = 'attachment; filename=%s' % name
        return response
