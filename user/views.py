from django.shortcuts import render
from user.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import (
        HttpResponseRedirect,
        HttpResponse,
        Http404,
        JsonResponse
        )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print user
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Account disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'user/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login')

def register(request):
    #is registration successful
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #hash password
            user.set_password(user.password)
            user.save()

            # commit - we need to set the user attribute our selves
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'user/register.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
            })

