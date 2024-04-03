from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import userForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.models import Vendor
from vendor.form import vendorForm
from .utils import detectUser, send_verifaction_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
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
            #send verifiction email
            mail_subject = 'please verify the account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verifaction_email(request, user,mail_subject,email_template)
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
            #send verifiction email
            mail_subject = 'please verify the account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verifaction_email(request, user,mail_subject,email_template)
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

def activate(request, uidb64, token):
    #activate the user by setting the is_activate status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user  = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"congratulation! your account is activate")
        return redirect('MyAccount')
    else:
        messages.error(request,"invalid activation link")
        return redirect('MyAccount')
    
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            mail_subject = 'please verify the account'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verifaction_email(request, user,mail_subject,email_template)
            messages.success(request,"Email verifaction link send successfully")
            return redirect('login')
        else:
            messages.error(request,"Account doesnot exist")
            return redirect('forgotpassword')
    return render(request, "accounts/forgotpassword.html")


def reset_password_validation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "please reset your password")
        return redirect('reset_password')
    else:
        messages.error(request, "Link has been expired!")
        return redirect('MyAccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get("uid")
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request,'Password changed Successfully')
            return  redirect('login')
        else:
            messages.info(request,'Both Password Field Must be Same')
            return  redirect('reset_password')
    return render(request, "accounts/reset_password.html")