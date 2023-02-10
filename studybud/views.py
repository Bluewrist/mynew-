from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from.models import Room,Topic,Messages
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
# Create your views here.

def loginPage(request):
    page  = 'login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,'invalid credentials')


    context = { "page":page} 
    return render (request,'login_register.html',context)

def logOutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form =  UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"this was bull shit plese be serious")

    context =  {
        'form':form,
        
    }
    return render (request,'login_register.html',context)


def home(request):
    q =  request.GET.get('q') if request.GET.get('q') != None else ""
    rooms =  Room.objects.filter(Q(topic__name__icontains=q)|
                                Q(name__icontains=q)|
                                Q(description__icontains=q)
                                )
    topic =  Topic.objects.all()
    room_count  =  rooms.count()

    context =  {
        'room':rooms,
        'topics':topic,
        'room_count':room_count,
    }
    return render(request,"home.html",context)


def room(request,pk):
    room =  Room.objects.get(id= pk)
    room_message =  room.messages_set.all().order_by('-created')
    participants  = room.participants.all()

    if request.method == "POST":
        massage = Messages.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect ('room', pk=room.id)
    

    context =  {
        'room':room,
        'room_message':room_message,
        'participants':participants ,
    }
    return render(request , "room.html",context)


def createRoom(request):
    form =  RoomForm()
    if request.method == "POST":
        form =  RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('home')
    context =  {'form':form}
    return render(request,'room-form.html',context)


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        form =  RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect ('home')
    form =  RoomForm(instance=room)
    
    context =  {'form':form}
    return render(request,'room-form.html',context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect ('home')
    return render(request,'delete.html',{'obj':room})
