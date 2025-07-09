from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from .models import UserProfile, Address
from orders.models import Order


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                user.first_name = request.POST.get('first_name', '')
                user.last_name = request.POST.get('last_name', '')
                user.email = request.POST.get('email', '')
                user.save()
                
                # UserProfile will be created automatically via signal
                
                # Log the user in
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Welcome {user.first_name or user.username}! Your account has been created.')
                    return redirect('core:home')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'core:home')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')


@login_required
def profile_view(request):
    """User profile view and edit"""
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        # Update user information
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Update profile information
        profile.phone = request.POST.get('phone', '')
        profile.address_line_1 = request.POST.get('address_line_1', '')
        profile.address_line_2 = request.POST.get('address_line_2', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.country = request.POST.get('country', '')
        profile.email_notifications = bool(request.POST.get('email_notifications'))
        profile.sms_notifications = bool(request.POST.get('sms_notifications'))
        profile.newsletter_subscription = bool(request.POST.get('newsletter_subscription'))
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('accounts:profile')
    
    # Get user's recent orders
    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'profile': profile,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_view(request):
    """User dashboard with overview of orders and profile"""
    user = request.user
    
    # Get user statistics
    total_orders = Order.objects.filter(user=user).count()
    pending_orders = Order.objects.filter(user=user, status='pending').count()
    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:3]
    
    context = {
        'user': user,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def addresses_view(request):
    """Manage user addresses"""
    user = request.user
    addresses = Address.objects.filter(user=user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            address = Address(
                user=user,
                title=request.POST.get('title', ''),
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                company=request.POST.get('company', ''),
                address_line_1=request.POST.get('address_line_1', ''),
                address_line_2=request.POST.get('address_line_2', ''),
                city=request.POST.get('city', ''),
                state=request.POST.get('state', ''),
                postal_code=request.POST.get('postal_code', ''),
                country=request.POST.get('country', ''),
                phone=request.POST.get('phone', ''),
                is_default=bool(request.POST.get('is_default'))
            )
            
            # If this is set as default, unset other defaults
            if address.is_default:
                Address.objects.filter(user=user, is_default=True).update(is_default=False)
            
            address.save()
            messages.success(request, 'Address added successfully!')
            
        elif action == 'delete':
            address_id = request.POST.get('address_id')
            try:
                address = Address.objects.get(id=address_id, user=user)
                address.delete()
                messages.success(request, 'Address deleted successfully!')
            except Address.DoesNotExist:
                messages.error(request, 'Address not found.')
        
        return redirect('accounts:addresses')
    
    context = {
        'addresses': addresses,
    }
    
    return render(request, 'accounts/addresses.html', context)
