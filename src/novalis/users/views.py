from django.shortcuts import render, redirect
from .forms import UserForm, CompanyForm, LoginForm
from django.contrib.auth import hashers, login, authenticate, logout
from .models import Company, User
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from .mixins import GroupRequiredMixin


def logout_view(request):
    logout(request)
    return redirect('/')


def gatekeeper_view(GroupRequiredMixin, request):
    pass






@unauthenticated_user
def login_view(request):
    valuenext = request.POST.get('next')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and valuenext != '':
            login(request, user)
            return redirect(valuenext)
        elif user is not None and valuenext == '':
            login(request, user)
            return redirect('/posts')
    var = {
        'form': form
    }
    return render(request, 'login.html', var)


@unauthenticated_user
def registration_view(request):
    form = CompanyForm(request.POST or None)
    user_form = UserForm(request.POST or None)
    if form.is_valid():
        company = form.cleaned_data.get('name').lower()
        try:
            company = Company.objects.get(name=company)
        except Company.DoesNotExist:
            company = form.save()
            company_registered = False
        else:
            company_registered = True
        var = {
            'user_form': UserForm(),
            'company': company,
            'company_registered':company_registered,
        }
        return render(request, 'user_registry.html', var)

    if request.POST.get('userform') == 'submitted':
        if user_form.is_valid():
            password = user_form.cleaned_data.get('password2')
            fname = user_form.cleaned_data.get('first_name')
            lname = user_form.cleaned_data.get('last_name')
            email = user_form.cleaned_data.get('email')
            company_id = request.POST.get('company_id')
            new_user = User.objects.create_user(
                email=email,
                password=password,
                first_name=fname,
                last_name=lname,
                username=email,
                company=Company.objects.get(id =company_id))
            if not Company.objects.get(id=company_id).has_manager:
                var = {
                    'company': Company.objects.get(id=company_id),
                    'user': new_user
                }
                return render(request, 'set_manager.html', var)
            return redirect('/posts')
        var = {
            'user_form': user_form,
        }
        return render(request, 'user_registry.html', var)

    if request.POST.get('answer'):
        company_tomg = Company.objects.get(id = request.POST.get('answer'))
        company_tomg.has_manager = True
        company_tomg.save()
        manager_group = Group.objects.get(name='manager')
        User.objects.get(id=request.POST.get('user')).groups.add(manager_group)
        user = User.objects.get(id=request.POST.get('user'))
        user.is_manager = True
        user.save()
        return redirect('/posts')

    else:
        var = {'form': form}
        return render(request, 'company_registry.html', var)


