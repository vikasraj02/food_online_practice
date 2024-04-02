from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import userForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.models import Vendor
from vendor.form import vendorForm
# Create your views here .

def registerUser(request):
    if request.method == 'POST':
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
    if request.method == 'POST':
        form = userForm(request.POST)
        v_form = vendorForm(request.POST, request.FILES)
        print(v_form.errors)
        if form.is_valid():
            print("form valid")
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