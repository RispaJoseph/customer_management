# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import Customer, Maker, Checker
from .forms import CustomerForm, UserRegistrationForm, MakerRegistrationForm, CheckerRegistrationForm

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user is not None:
            if hasattr(user, 'maker'):
                return user
            elif hasattr(user, 'checker'):
                return user
        return None

def maker_registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        maker_form = MakerRegistrationForm(request.POST)
        if user_form.is_valid() and maker_form.is_valid():
            user = user_form.save()
            maker = maker_form.save(commit=False)
            maker.user = user
            maker.save()
            return redirect('maker_login')
    else:
        user_form = UserRegistrationForm()
        maker_form = MakerRegistrationForm()
    return render(request, 'maker_registration.html', {'user_form': user_form, 'maker_form': maker_form})

def checker_registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        checker_form = CheckerRegistrationForm(request.POST)
        if user_form.is_valid() and checker_form.is_valid():
            user = user_form.save()
            checker = checker_form.save(commit=False)
            checker.user = user
            checker.save()
            return redirect('checker_login')
    else:
        user_form = UserRegistrationForm()
        checker_form = CheckerRegistrationForm()
    return render(request, 'checker_registration.html', {'user_form': user_form, 'checker_form': checker_form})


def maker_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'maker'):
            login(request, user)
            return redirect('maker_dashboard')  # Redirect to maker dashboard
        else:
            return render(request, 'maker_login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'maker_login.html')

def checker_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'checker'):
            login(request, user)
            return redirect('checker_dashboard')  # Redirect to checker dashboard
        else:
            return render(request, 'checker_login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'checker_login.html')

@login_required
def dashboard(request):
    if hasattr(request.user, 'maker'):
        customers = Customer.objects.filter(maker=request.user.maker)
    elif hasattr(request.user, 'checker'):
        makers = request.user.checker.makers.all()
        customers = Customer.objects.filter(maker__in=makers)
    else:
        customers = None
    return render(request, 'dashboard.html', {'customers': customers})

@login_required
def upload_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.maker = request.user.maker
            customer.save()
            return redirect('maker_dashboard')
    else:
        form = CustomerForm()
    return render(request, 'upload_customer.html', {'form': form})

@login_required
def review_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            customer.status = Customer.APPROVED
        elif action == 'decline':
            customer.status = Customer.DECLINED
        customer.save()
        return redirect('dashboard')
    return render(request, 'review_customer.html', {'customer': customer})


@login_required
def maker_dashboard(request):
    customers = Customer.objects.filter(maker=request.user.maker)
    return render(request, 'maker_dashboard.html', {'customers': customers})

@login_required
def checker_dashboard(request):
    makers = request.user.checker.makers.all()
    customers = Customer.objects.filter(maker__in=makers).distinct()  # Ensure only unique customers
    return render(request, 'checker_dashboard.html', {'customers': customers})


@login_required
def approve_decline_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return redirect('checker_dashboard')  # Or handle the error as needed

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approved':
            customer.status = Customer.APPROVED
        elif action == 'declined':
            customer.status = Customer.DECLINED
        customer.save()
        return redirect('checker_dashboard')

    return render(request, 'approve_decline_customer.html', {'customer': customer})
