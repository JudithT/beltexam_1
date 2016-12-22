from django.shortcuts import render, HttpResponse, redirect
from .models import User, Message, Favorite

from django.contrib import messages


def index(request):
    allusers = User.objects.all()



    print "all the users in the database"
    for user in allusers:
        print user.id, user.first_name, user.last_name, user.email

    # myuser = User.objects.get(id=1)
    # mynewmessage = Message.objects.create(message="My first message", user = myuser, author="Albert Einstein")
    # print "Made a new message", mynewmessage
    mymessage = Message.objects.get(id=1)
    print mymessage.message, mymessage.user, mymessage.author

    return render(request, "registration/index.html")

def register(request):
    newuser = ""
    result = User.objects.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm'], request.POST['birthday'])
    if result[0] == True:
        request.session['email'] = request.POST['email']
        request.session['id'] = result[1].id

        try:
            request.session.pop('errors')
        except:
            a=1
        return redirect('/quotes')
    else:
        request.session['errors'] = result[1]
        return redirect('/')


def login(request):
    loggedin = ""
    print "made it to login"
    result = User.objects.login(request.POST['email'], request.POST['password'])
    if result[0] == True:
        # if we got true back, then result[1] is our user
        request.session['email'] = request.POST['email']
        request.session['id'] = result[1].id
        try:
            request.session.pop('errors')
        except:
            pass
        print "got the new id for logged in user", request.session['id']
        return redirect('/quotes')
    else:
        request.session['errors'] = result[1]
        return redirect('/')



def quotes(request):
    if 'id' in request.session:
        print "made it to success", request.session['id']
        email = request.session['email']
        print "session's email", email
        context={
        #user is the user who is logged in.
        "user":User.objects.filter(email=email),
        "messages":Message.objects.all(),
        "favorites":Favorite.objects.all()
        }
    else:
        return redirect('/')


    # request.session['message']=request.POST['message']
    # message = request.POST['message']
    # print "session's quote",quote
    # user = User.objects.filter(email=email)[0]
    # message = Message.objects.filter(message=message)
    # context = {
        # "message": Message.objects.all()

    # }
    return render(request, 'registration/success.html', context)


def process(request):
    print "you made it to quotes"
    myuser = User.objects.get(id=request.session['id'])
    print "session id", request.session['id']
    # User.objects.get(id=request.session['id'])
    message = Message.objects.create(message=request.POST['message'],author=request.POST['author'],user = myuser)

    return redirect('/quotes')


def users(request, id):
    print "you made it to userpage", id
    user = User.objects.get(id=id)
    messages=Message.objects.filter(user=user)
    context={

    "user": user,
    "messages":messages,
    "count":len(messages)

    }

    return render(request, 'registration/users.html', context)

def createfavorite(request):
    print" you made it to favorites"
    user = User.objects.get(id=request.session['id'])
    messages=request.POST['backgrounddata']
    print messages
    # A=message.message__messages
    # print A
    favoritemessage=Message.objects.get(id=messages)
    favorites=Favorite.objects.create(user=user, message=favoritemessage)
    print favorites
    person=favorites.user.first_name
    message=favorites.message.message
    print "person!!!!!!!!!!!", person
    print "message!!!!!!!!!!!!", message



    return redirect('/quotes')

def removefavorite(request):
    print" you made it to removefavorite"
    user = User.objects.get(id=request.session['id'])
    message=request.POST['removefavorite']
    deletefavorite=Favorite.objects.get(id=message).delete()
    print"favorite is removed"

    return redirect('/quotes')



def logout(request):

    session.clear()

    return redirect('/')
