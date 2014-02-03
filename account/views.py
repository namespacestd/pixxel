from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from devfest.models import CreateAccountForm, UserAccount
from django.contrib.auth.forms import *
from django.contrib import auth

import logging

logger = logging.getLogger('root.' + __name__)

def new_account(request):
    return render(request, 'account/new_account.html')

def login_page(request):
    return render(request, 'account/login_page.html')

def login(request):
    if request.method == 'POST':  # If the form has been submitted...

        AuthenticationForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponse('Success')
            else:
                error_msg = 'Your account has been disabled.'
        else:
            error_msg = "Your username and password didn't match. Please try again."

        logger.info('Login failed. User: %s, Reason: %s', username, error_msg)
        return HttpResponse(error_msg)
    else:
        return HttpResponse('No login page. Must be posted to by login form.')


def create(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = CreateAccountForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                user = auth.authenticate(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password2'])
                auth.login(request, user)

                new_account = UserAccount.find(form.cleaned_data['username'])
                logger.info('User Create successful. User: %s', new_account)

                return HttpResponse('Success') 
            else:
                logger.error('User Create failed. Invalid form.')
                raise Exception(form.errors.as_ul())
        except Exception as ex:
            logger.error('User Create failed. Validation or Authentication failed.')
            return render(request, "account/new_account.html", { 'errors' : ex.message })
    else:
        logger.error('User Create failed. Invalid form submission.')
        return HttpResponse('Account creation failed.')

def logout(request):
    user = request.user
    auth.logout(request)
    logger.info('Logout. User: %s', user)
    return HttpResponseRedirect('/')