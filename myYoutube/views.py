# import mimetypes
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django import forms
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from myYoutube.models import VideoUrl
from myYoutube.forms import UploadFileForm,UserForm
from django.template import RequestContext
from django.http import HttpResponse
import boto
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from ratings.handlers import ratings
import re
from django.conf import urls


# from django.utils import simplejson
# from django.core import serializers



def one_time():
    print 'hello word!'
    try:
        s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = s3.create_bucket('xz820')
    except boto.exception.S3CreateError,e:
        print e.message

    c = boto.connect_cloudfront()
    origin = boto.cloudfront.origin.S3Origin('xz820.s3.amazonaws.com')
    distro = c.create_distribution(origin=origin, enabled=True, comment='My new Distribution')

    strdistro = c.create_streaming_distribution(origin=origin, enabled=True, comment='My new streaming Distribution')
    print distro.domain_name
    print strdistro.domain_name
#     c = boto.connect_cloudfront(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
#     origin = boto.cloudfront.origin.S3Origin('xz820.s3.amazonaws.com')
#     distro = c.create_distribution(origin=origin, enabled=False, comment='My new Distribution')
    settings.web_url ="http://"+distro.domain_name+"/"
    print settings.web_url
    settings.rmtp_url="rtmp://"+strdistro.domain_name+"/cfx/st/"
    print settings.rmtp_url
    # settings.web_url ="http://dniq4izi0hlk0.cloudfront.net/"
    # print settings.web_url
    # settings.rmtp_url="rtmp://swin77cy85iad.cloudfront.net/cfx/st/"
    # print settings.rmtp_url




def index(request):
    # print urls.W
    # print settings.AWS_ACCESS_KEY_I
    context = RequestContext(request)
    videos = VideoUrl.objects.all().order_by("-score")
    if not request.method == "POST":
        f = UploadFileForm()
        return render_to_response('myYoutube/index.html', {'form':f, 'videos':videos},context)
    f = UploadFileForm(request.POST, request.FILES)
    if not f.is_valid():
        return render_to_response('myYoutube/index.html', {'form':f, 'videos':videos},context)
    file = request.FILES['file']
    filename = file.name
    result = re.match(r'.+\.mp4',filename)
    print 123
    if not result:
        message = "please upload a mp4 type!"
        return render_to_response('myYoutube/index.html', {'form':f, 'videos':videos, 'message':message},context)

    content = file.read()
    store_in_s3(filename, content,context)




    # v = VideoUrl(name= filename,url="http://dniq4izi0hlk0.cloudfront.net/" + filename,stream_url="rtmp://swin77cy85iad.cloudfront.net/cfx/st/"+filename)
    v = VideoUrl(name= filename,url=settings.web_url+ filename,stream_url=settings.rmtp_url+filename)


    # v = VideoUrl(name= filename,url=settings.V + filename)

    v.save()




    videos = VideoUrl.objects.all().order_by("-score")

    return render_to_response('myYoutube/index.html', {'form':f, 'videos':videos},context)


def store_in_s3(filename, content,context):
        s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucket = s3.get_bucket('xz820')
        k = Key(bucket)
        k.key = filename
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
            s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
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
    if request.method=='POST':
        a = request.FILES['fruit']
        print a
    if request.method=='GET':
        if 'url' in request.GET:
            url=request.GET['url']
            context_dict['url']=url
            cur = VideoUrl.objects.get(url=url)
            # print cur.stream_url
            context_dict['stream_url']=cur.stream_url

    return render_to_response('myYoutube/watch.html',context_dict,context)

def register(request):
    # if request.session.test_cookie_worked():
    #     print ">>>> TEST COOKIE WORKED!"
    #     request.session.delete_test_cookie()

    context= RequestContext(request)


    registered = False

    if request.method =='POST':

        user_form = UserForm(data=request.POST)

        if user_form.is_valid():

            user=user_form.save()

            user.set_password(user.password)
            user.save()

            registered= True

        else:
            print user_form.errors
    else:
        user_form=UserForm()


    context_dict={'user_form':user_form,'registered':registered}

    return render_to_response('myYoutube/register.html',context_dict, context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/myYoutube/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('myYoutube/login.html', {}, context)
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/myYoutube/')































