from django.shortcuts import render,redirect

from accounts.models import Account
from accounts.form import RegistrationForm, VerifyForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages,auth
from accounts.verify import send,check

# Create your views here.
def register(request):
    print(request.POST)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            phone_number  = form.cleaned_data['phone_number']
            email  = form.cleaned_data['email']
            password  = form.cleaned_data['password']
            username=email.split("@")[0]
            user= Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
            user.phone_number = phone_number
            
            user.save()
            
            #user activation
            send(phone_number)
            messages.success(request,'Registration successful')
            return redirect('')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request,'register.html',context)
def verification(request):
    if request.method == 'POST':
        
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_number= request.session['phone_number']
            if check(phone_number, code):
                user=Account.objects.get(phone_number=phone_number)
                user.is_active = True
                user.save()
                return redirect('login')
    else:
        form = VerifyForm()
    return render(request, 'verification.html', {'form': form})
def loginView(request):
    return render(request,'login.html')