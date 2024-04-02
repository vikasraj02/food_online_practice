from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import userForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.models import Vendor
from vendor.form import vendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here .

# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "your are alredy loggedin!")
        return redirect("MyAccount")
    elif request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('registerUser')
        else:
            print("in valid")
            print(form.errors)
    else:
        form = userForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registeruser.html',context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "your are alredy loggedin!")
        return redirect("MyAccount")
    elif request.method == 'POST':
        form = userForm(request.POST)
        v_form = vendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,"your account has been rgistered please wait for vetification")
            return redirect('registerVendor')
        else:
            print("invaliid form")
            print(form.errors)
    else:
        form = userForm()
        v_form = vendorForm()
    context = {
        "form":form,
        "v_form" : v_form,
    }
    return render(request, 'accounts/registervendor.html',context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"your are alredy loggedin")
        return redirect('MyAccount')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Your now logged in")
            return redirect('MyAccount')
        else:
            messages.error(request, "invalid credentials")
            return redirect("login")
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request,"Your are now loggedout")
    return redirect('login')

@login_required(login_url='login')
def MyAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')