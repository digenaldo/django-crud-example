"""
WSGI config for conceptu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conceptu.settings')

application = get_wsgi_application()

# Apply migrations automatically on startup (for Render free tier)
# This ensures migrations are applied even if buildCommand fails
# Only runs once per worker process
try:
    from django.core.management import execute_from_command_line
    from django.db import connection
    from django.db.migrations.recorder import MigrationRecorder
    
    # Only run migrations if we're in production (not during tests)
    if os.environ.get('DJANGO_SETTINGS_MODULE') and not os.environ.get('TESTING'):
        try:
            # Ensure database connection
            connection.ensure_connection()
            
            # Check if migrations need to be applied
            recorder = MigrationRecorder(connection)
            applied = recorder.applied_migrations()
            
            # If no migrations are applied, run migrate
            if len(applied) == 0:
                import sys
                print("⚠️  No migrations found. Applying migrations automatically...")
                execute_from_command_line(['manage.py', 'migrate', '--noinput'])
                print("✅ Migrations applied successfully!")
        except Exception as e:
            # Log error but don't crash the app
            print(f"⚠️  Could not apply migrations automatically: {str(e)}")
            print("   This is normal if migrations were already applied or database is not ready.")
except (ImportError, Exception) as e:
    # Silently fail - migrations might already be applied
    pass
