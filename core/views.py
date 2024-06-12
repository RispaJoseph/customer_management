from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer, Maker, Checker
from .forms import CustomerForm

@login_required
def dashboard(request):
    if hasattr(request.user, 'maker'):
        customers = Customer.objects.filter(maker=request.user.maker)
    elif hasattr(request.user, 'checker'):
        makers = request.user.checker.makers.all()
        customers = Customer.objects.filter(maker__in=makers)
    else:
        customers = None
    return render(request, 'core/dashboard.html', {'customers': customers})

@login_required
def upload_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.maker = request.user.maker
            customer.save()
            return redirect('dashboard')
    else:
        form = CustomerForm()
    return render(request, 'core/upload_customer.html', {'form': form})

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
    return render(request, 'core/review_customer.html', {'customer': customer})
