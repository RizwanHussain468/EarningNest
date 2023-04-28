from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Deposit, UserDashboard

def home(request):
    context = { 
        'user': request.user   
    }
    return render(request,'index.html', context)

@login_required(login_url='login')
def dashboard(request):
    try:
        dashboard = UserDashboard.objects.get(user=request.user)
        deposits = Deposit.objects.filter(user=request.user)
        context = {
            'user': request.user, 
            'dashboard': dashboard,
            'deposits': deposits,
            'refferal': request.user.get_uidb64()
        }
        return render(request,'userdashboard.html', context)
    except:
        context = {'user': request.user, 'refferal': request.user.get_uidb64()}
        return render(request,'userdashboard.html', context)

@login_required(login_url='login')
def about(request):
    context = {'user': request.user}
    return render(request,'about-us.html', context)

@login_required(login_url='login')
def services(request):
    context = {'user': request.user}
    return render(request,'services.html', context)

@login_required(login_url='login')
def profit_chart(request):
    context = {'user': request.user}
    return render(request,'portfolio.html', context)

@login_required(login_url='login')
def faqs(request):
    context = {'user': request.user}
    return render(request,'faq.html', context)


def contact_us(request):
    context = {'user': request.user}
    return render(request,'contact-us.html', context)

@login_required(login_url='login')
def profile(request):
    date = CustomUser.objects.get(id=request.user.id).datetime.date()
    context = { 
        'user': request.user, 
        'date': date, 
    }
    return render(request,'userprofile.html', context)

@login_required(login_url='login')
def deposit(request):
    deposits = Deposit.objects.filter(user=request.user)
    context = {
            'user': request.user, 
            'deposits': deposits,
    }
    return render(request,'deposit.html', context)

@login_required(login_url='login')
def withdraw(request):
    return render(request,'withdraw.html')

@login_required(login_url='login')
def refferals(request):
    return render(request,'refferals.html')

@login_required(login_url='login')
def profit_share(request):
    return render(request,'profitshare.html')

@login_required(login_url='login')
def reinvest_portfolio(request):
    return render(request,'reinvest_portfolio.html')

@login_required(login_url='login')
def donations(request):
    return render(request,'donations.html')

@login_required(login_url='login')
def promo_achievement(request):
    return render(request,'promo_achievement.html')

def admin_view(request):
    admin_url = reverse('admin:index')
    return redirect(admin_url)

def logoutUser(request):
	logout(request)
	return redirect('login')

def registration(request):
    return render(request,'registration.html')

def sign_in(request):
    return render(request,'career.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password_confirm']
        cnic = request.POST['cnic']
        phone = request.POST['phone']
        next_of_kin = request.POST['nextofkinname']
        next_of_kin_phone = request.POST['nextofkinphone']

        # Perform validation and error handling
        if not username:
            messages.error(request, 'Username is required.')
            return redirect('register')

        if not email:
            messages.error(request, 'Email is required.')
            return redirect('register')

        if not password:
            messages.error(request, 'Password is required.')
            return redirect('register')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if not cnic:
            messages.error(request, 'CNIC is required.')
            return redirect('register')

        if not phone:
            messages.error(request, 'Contact number is required.')
            return redirect('register')

        if not next_of_kin:
            messages.error(request, 'Next of kin name is required.')
            return redirect('register')

        if not next_of_kin_phone:
            messages.error(request, 'Next of kin phone number is required.')
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            return redirect('register')

        user = CustomUser.objects.create_user(username=username, email=email, password=password, 
                                              phone=phone, cnic_no=cnic, next_of_kin=next_of_kin, 
                                              next_of_kin_phone=next_of_kin_phone, datetime=timezone.now())
        user.set_password(password)
        user.save()

        messages.success(request, 'Account created successfully.')
        return render(request, 'career.html')
    else:
        return render(request, 'registration.html')

def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password =request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Email OR password is incorrect')
                
    context = {}
    return render(request, 'career.html', context)

