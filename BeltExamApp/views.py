from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Quote

def index(request):
    return render(request, 'index.html')

def quotes(request):
    if 'loggedInUserID' not in request.session:
        messages.error(request, 'You must be logged in to view the page')
        return redirect('/')

    context = {
        'loggedInUser': User.objects.get(id = request.session['loggedInUserID']),
        'quotes': Quote.objects.all(),
    }
    return render(request, 'quotes.html', context)

def registration(request):
    errorsFromValidator = User.objects.basic_validator(request.POST)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/')

    newUser = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = request.POST['password'])

    request.session['loggedInUserID'] = newUser.id

    return redirect('/quotes')


def login(request):
    errorsFromValidator = User.objects.login_validator(request.POST)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/')
    print('*************')
    print(request.POST)
    print('*************')
    test = User.objects.filter(email = request.POST['email'])
    request.session['loggedInUserID'] = test[0].id
    return redirect('/quotes')


def logout(request):
    del request.session['loggedInUserID']
    return redirect('/')

def addQuote(request):
    print('**************')
    print(Quote.objects.all())
    print('**************')
    errorsFromValidator = Quote.objects.quote_validator(request.POST)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/quotes')
    Quote.objects.create(author = request.POST['author'], actual_quote = request.POST['quote'], posted_by = User.objects.get(id = request.session['loggedInUserID']))
    return redirect('/quotes')

def delete(request, quoteid):
    deletedQuote = Quote.objects.get(id = quoteid)
    deletedQuote.delete()
    return redirect('/quotes')

def editUserPage(request, userid):
    context = {
        'users': User.objects.get(id = userid),
    }
    return render(request, 'editUser.html', context)

def editUser(request, userid):
    errorsFromValidator = User.objects.update_validator(request.POST, User.objects.get(id=request.session['loggedInUserID']))
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect(f'/edit/myaccount/{userid}')
    context = {
        'users': User.objects.get(id = userid)
    }
    updatedUser = User.objects.get(id = userid)
    updatedUser.first_name = request.POST['first_name']
    updatedUser.last_name = request.POST['last_name']
    updatedUser.email = request.POST['email']
    updatedUser.save()
    return redirect('/quotes')

def users(request, userid):
    thisUser = User.objects.get(id = userid)
    context = {
        'uploadedQuotes': thisUser.uploaded_quote.all(),
        'users': User.objects.get(id = userid)
    }
    return render(request, 'user.html', context)

def likeQuote(request, quoteid):
    thisUser = User.objects.get(id = request.session['loggedInUserID'])
    thisQuote = Quote.objects.get(id = quoteid)
    thisUser.liked_quotes.add(thisQuote)
    likes = thisQuote.users_who_like.all()
    numLikes = len(likes)
    print(numLikes)
    addNumLikes = Quote.objects.get(id = quoteid)
    addNumLikes.numLikes = numLikes
    addNumLikes.save()
    return redirect('/quotes')