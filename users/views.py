# -*- coding: utf-8 -*-
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db import connection

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
                # Check if database is accessible
                from django.db import connection
                connection.ensure_connection()
                
                # Try to save user
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created successfully for {username}! Please sign in to continue.')
                return redirect('login')
            except Exception as e:
                # Get detailed error information
                import traceback
                error_msg = str(e)
                error_type = type(e).__name__
                full_traceback = traceback.format_exc()
                
                # Log the error
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Registration error: {error_type} - {error_msg}\n{full_traceback}')
                
                # Show user-friendly error with details if DEBUG is True
                if os.environ.get('DEBUG', 'False') == 'True':
                    messages.error(request, f'Error: {error_type} - {error_msg}')
                else:
                    messages.error(request, 'An error occurred while creating your account. The database may not be properly configured. Please check if migrations were applied.')
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

@csrf_exempt
def debug_info(request):
    """Debug endpoint to check database and migrations status"""
    from django.conf import settings
    from django.db import connection
    from django.contrib.auth.models import User
    import traceback
    
    info = {
        'database_engine': settings.DATABASES['default']['ENGINE'],
        'database_name': settings.DATABASES['default'].get('NAME', 'N/A'),
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
    }
    
    # Test database connection
    try:
        connection.ensure_connection()
        info['database_connected'] = True
    except Exception as e:
        info['database_connected'] = False
        info['database_error'] = str(e)
    
    # Check if auth_user table exists
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
            table_exists = cursor.fetchone() is not None
            info['auth_user_table_exists'] = table_exists
            
            if table_exists:
                cursor.execute("SELECT COUNT(*) FROM auth_user;")
                user_count = cursor.fetchone()[0]
                info['user_count'] = user_count
    except Exception as e:
        info['auth_user_table_exists'] = False
        info['table_check_error'] = str(e)
    
    # Check migrations
    try:
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        applied_migrations = recorder.applied_migrations()
        info['applied_migrations_count'] = len(applied_migrations)
        info['applied_migrations'] = [str(m) for m in list(applied_migrations)[:10]]  # First 10
    except Exception as e:
        info['migrations_check_error'] = str(e)
    
    return JsonResponse(info, status=200)
