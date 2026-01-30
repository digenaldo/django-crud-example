# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            next_url = request.GET.get('next', 'product_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')

@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created successfully for {username}! Please sign in to continue.')
                return redirect('login')
            except Exception as e:
                # Log the error for debugging
                import logging
                import traceback
                logger = logging.getLogger(__name__)
                logger.error(f'Registration error: {str(e)}\n{traceback.format_exc()}')
                messages.error(request, f'An error occurred while creating your account. Please try again or contact support.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@csrf_exempt
def health_check(request):
    """Health check endpoint for Render monitoring"""
    return JsonResponse({'status': 'ok'}, status=200)
