from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Document
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.db import IntegrityError

def editor(request):
    docid = int(request.GET.get('docid', 0))
    documents = Document.objects.all()

    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')

        if docid > 0:
            document = Document.objects.get(pk=docid)
            document.title = title
            document.content = content
            document.save()

            return redirect('/?docid=%i' % docid)
        else:
            document = Document.objects.create(title=title, content=content)

            return redirect('/?docid=%i' % document.id)

    if docid > 0:
        document = Document.objects.get(pk=docid)
    else:
        document = ''

    context = {
        'docid': docid,
        'documents': documents,
        'document': document
    }

    return render(request, 'editor.html', context)

def delete_document(request, docid):
    document = Document.objects.get(pk=docid)
    document.delete()
    return redirect('/?docid=0')

def Register(request):
  if request.method=="POST":
    if request.POST.get('password1')==request.POST.get('password2'):
      try:
        saveuser=User.objects.create_user(request.POST.get('username'),password=request.POST.get('password1'))
        saveuser.save()
        return render(request,'register.html',{'form':UserCreationForm(),'info':'The user'+' '+request.POST.get('username')+' successfully registered...!'})
      except IntegrityError:
        return render(request,'register.html',{'form':UserCreationForm(),'error':'The user'+' '+request.POST.get('username')+' already exist...!'})
    else:
      return render(request,'register.html',{'form':UserCreationForm(),'error':'The Passwords Are Not Matching..!'})  
  else:
    return render(request,'register.html',{'form':UserCreationForm})

def userlogin(request):
    if request.method=="POST":
        loginsucess=authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
        if loginsucess is None:
            return render(request,'login.html',{'form':AuthenticationForm(),'error':'invalid username and password'})
        else:
            login(request,loginsucess)
            return redirect('editor')
    else:
        return render(request,'login.html',{'form':AuthenticationForm()})

def about(request):
    return render(request,"about.html")