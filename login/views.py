
# Create your views here.
# views.py
from login.forms import RegistrationForm, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

saved_user = ""
saved_pass = ""
session_user_pass_map = {}


@csrf_exempt
def receivePassword(request):
    global saved_pass
    if request.method == 'POST':
        passPlain = request.POST.get('pass')
        saved_pass = passPlain
        return HttpResponse('')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration/register.html',
        variables,
    )


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def home(request):
    global saved_user, session_user_pass_map
    saved_user = str(request.user.username)
    request.session['def_username'] = saved_user
    session_user_pass_map[saved_user] = saved_pass
    print 'set : ', saved_user, ' also: ', saved_pass
    return redirect('/editor/')
