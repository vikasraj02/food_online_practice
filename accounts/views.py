from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import userForm
from .models import User
from django.contrib import messages

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