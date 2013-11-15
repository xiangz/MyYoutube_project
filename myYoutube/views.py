import mimetypes
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django import forms
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from myYoutube.models import VideoUrl
from myYoutube.forms import UploadFileForm
from django.template import RequestContext
from django.http import HttpResponse
import boto
from django.utils import simplejson
from django.core import serializers




def index(request):
    context = RequestContext(request)

    videos = VideoUrl.objects.all().order_by("-uploaded")
    # data = serializers.serialize("xml", videos)

    # for video in videos:
    #      video.url=

    if not request.method == "POST":
        f = UploadFileForm()
        return render_to_response('myYoutube/index.html', {'form':f, 'videos':videos},context)

    f = UploadFileForm(request.POST, request.FILES)
    if not f.is_valid():
        return render_to_response('myYoutube/index.html', {'form':f, 'videos':videos},context)
    file = request.FILES['file']
    filename = file.name
    content = file.read()
    store_in_s3(filename, content,context)
    v = VideoUrl(name= filename,url="http://xz820.s3.amazonaws.com/" + filename)
    v.save()

    videos = VideoUrl.objects.all().order_by("-uploaded")

    return render_to_response('myYoutube/index.html', {'form':f, 'videos':videos},context)


def store_in_s3(filename, content,context):
        print 9
        # conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        # b = conn.create_bucket('xzz820')
        s3 = boto.connect_s3()
        bucket = s3.get_bucket('xz820')
        k = Key(bucket)
        # mime = mimetypes.guess_type(filename)[0]
        # k = Key(b)
        k.key = filename
        # k.set_metadata("Content-Type", mime)
        k.set_contents_from_string(content)
        k.set_acl("public-read")

def deleteVideo(request):
    context = RequestContext(request)
    if request.method=='GET':
        # print 1
        key=request.GET['key']
        # print 2
        if key:
            print key
            s3 = boto.connect_s3()
            bucket = s3.get_bucket('xz820')
            k = Key(bucket)
            k.key=key
            k.delete()
            b = VideoUrl.objects.get(name=key)
            b.delete()
    videos = VideoUrl.objects.all().order_by("-uploaded")



    return render_to_response('myYoutube/video_list.html',{'videos':videos},context)

def watch(request):
    context = RequestContext(request)
    context_dict={}
    if request.method=='GET':
        if 'url' in request.GET:
            url=request.GET['url']
            context_dict['url']=url

    return render_to_response('myYoutube/watch.html',context_dict,context)

































