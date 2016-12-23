from django.shortcuts import render, HttpResponse, redirect
from .models import User, Message, Favorite

from django.contrib import messages


def index(request):
    return render(request, "registration/index.html")

def register(request):
    result = User.objects.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm'], request.POST['birthday'])
    if result[0] == True:
        request.session['email'] = request.POST['email']
        request.session['id'] = result[1].id
        return redirect('/quotes')
    else:
        for message in result[1]:
            messages.error(request, message)
        return redirect('/')


def login(request):
    loggedin = ""
    print "made it to login"
    result = User.objects.login(request.POST['email'], request.POST['password'])
    if result[0] == True:
        # if we got true back, then result[1] is our user
        request.session['email'] = request.POST['email']
        request.session['id'] = result[1].id
        print "got the new id for logged in user", request.session['id']
        return redirect('/quotes')
    else:
        for message in result[1]:
            messages.error(request, message)
        return redirect('/')



def quotes(request):
    if 'id' in request.session:
        print "made it to success", request.session['id']
        email = request.session['email']
        print "session's email", email
        user = User.objects.filter(email=email)[0]
        favs = Favorite.objects.filter(user = user)
        favs_ids = Favorite.objects.filter(user = user).values_list('message__id', flat=True)
        print favs_ids
        context={
            #user is the user who is logged in.
            "user": user,
            "messages":Message.objects.exclude(id__in=favs_ids),
            "favorites": favs
        }
    else:
        return redirect('/')

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
    context = {
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

    request.session.clear()

    return redirect('/')
