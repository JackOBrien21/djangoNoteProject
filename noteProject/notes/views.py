from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from notes.models import Note
from django.shortcuts import get_object_or_404
# Create your views here.

# def delete_user_entries(username):
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         return "User not found."
    
#     # delete entries in the database whose author field matches the user's name
#     user.entry_set.all().delete()
#     user.delete()
#     return "User and related entries have been deleted."
def index(request):
    username = request.user
    list_of_notes = Note.objects.filter(author=username)
    return render(request, "notes/index.html", {'username':username, 'list_of_notes':list_of_notes})

def signin(request):
    if (request.method == "POST"):
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            print("Here")
            login(request, user)
            
            list_of_notes = Note.objects.filter(author=username)
            return render(request, "notes/index.html", {'username' : username, 'list_of_notes': list_of_notes})
        else:
            error = "Your Information Didn't Match, Try Again"
            ctx = {'error':error}
            return render(request, 'notes/signin.html', ctx)

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
        if (pass1 == pass2):
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname

            myuser.save()

            messages.success(request, "Your Account has been successfully created")
            return redirect('/signin')
        else:
            error = "Your Password's Didn't Match, Try Again"
            ctx = {'error':error}
            return render(request, 'notes/index.html', ctx)
        
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
        print(username)
        title = request.POST['title']
        content = request.POST['content']
        newNote = Note(title=title, content=content, author=username)
        newNote.save()
        print("IT SHOULD HAVE SAVED")
        list_of_notes = Note.objects.filter(author=username)
        ctx = {'list_of_notes': list_of_notes, 'username':username}
        return render(request, "notes/index.html", ctx)
    return render(request, "notes/addnote.html", {'username':request.user})

def delete(request, id):
    if (request.method == 'POST'):
        note_instance = Note.objects.get(pk=id)
        note_instance.delete()
        list_of_notes = Note.objects.filter(author=request.user)
        ctx = {'list_of_notes': list_of_notes, 'username': request.user}
        # NOW WE WANT TO GET THE CORRESPONDING NOTE 
        return render(request, "notes/index.html", ctx)
    note_instance = Note.objects.get(pk=id)
    if note_instance is None:
        msg = "Failed to find the given note"
        ctx = {'msg':msg}
        return render(request, "notes/error.html", ctx)
    if str(note_instance.author) == str(request.user):
        ctx = {'note_instance':note_instance, 'username':request.user}
        return render(request, "notes/delete.html", ctx)
    else:
        msg = "You aren't authorized to access the requested note"
        ctx = {'msg' : msg}
        return render(request, "notes/error.html")

def detail(request, id):
    
    note_instance = get_object_or_404(Note, pk=id)
    if note_instance is not None and str(note_instance.author) == str(request.user):
        ctx = {'note_instance':note_instance, 'username':request.user}
        return render(request, "notes/detail.html", ctx)
    else:
        msg = "Failed to find the given note"
        ctx = {'msg' : msg}
        return render(request, "notes/error.html", ctx)
    
def update(request, id):
    note_instance = get_object_or_404(Note, pk=id)

    if (note_instance is None):
        msg = "Failed to find the given note"
        ctx = {'msg':msg}
        return render(request, "notes/error.html", ctx)
    
    if (request.method == 'POST' and str(note_instance.author) == str(request.user)):
        note_instance.title = request.POST['title']
        note_instance.content = request.POST['content']
        note_instance.save()
        list_of_notes = Note.objects.filter(author=request.user)
        ctx = {'list_of_notes': list_of_notes, 'username': request.user}
        return render(request, "notes/index.html", ctx)
    # JUST ROUTING TO /update/id bc dont want to change info if request==GET
    if str(note_instance.author) == str(request.user):
        ctx = {'note_instance':note_instance, 'username':request.user}
        return render(request, "notes/update.html", ctx)
    else:
        msg = "You aren't authorized to access the requested note"
        ctx = {'msg' : msg}
        return render(request, "notes/error.html")