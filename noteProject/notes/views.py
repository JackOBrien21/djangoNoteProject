from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from notes.models import Note
# Create your views here.
def index(request):
    return render(request, "notes/index.html")

def signin(request):
    if (request.method == "POST"):
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            return render(request, "notes/index.html", {'username' : username})
        else:
            messages.error(request, "Bad Credentials")
            return redirect('/signin')

    return render(request, "notes/signin.html")

def signup(request):
    if (request.method == "POST"):
        # username = request.POST.get('username') # WHATEVER THE NAME BUTE ON THE INPUT TAG IS
        username = request.POST['username'] # DOES SAME THING AS LINE ABOVE
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been successfully created")
        return redirect('/signin')
    return render(request, "notes/signup.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Succesfully")
    return redirect("/")

def addnote(request):
    if (request.method == 'POST'):
        # GONNA WANNA GRAB USERNAME like username = request.POST['username']
        # GONNA WANNA GRAB ALL NOTE MODELS with username = this.user.username

        username = request.user
        title = request.POST['title']
        content = request.POST['content']
        newNote = Note(title=title, content=content, author=username)
        newNote.save()
        list_of_notes = Note.objects.filter(author=username)
        ctx = {'list_of_notes': list_of_notes}
        return render(request, "notes/index.html", ctx)
    return render(request, "notes/addnote.html")