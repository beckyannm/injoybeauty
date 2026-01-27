"""
Configuration settings for InJoy Beauty backend.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database
DATABASE_PATH = BASE_DIR / 'database' / 'salon.db'

# Flask settings
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Database
    DATABASE = str(DATABASE_PATH)
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000').split(',')
    
    # Business settings
    BUSINESS_NAME = "InJoy Beauty"
    BUSINESS_TAGLINE = "Inclusive Beauty Services"
    BUSINESS_EMAIL = "jaymie.injoy.services@gmail.com"
    BUSINESS_PHONE = "613-868-6944"
    BUSINESS_LOCATION = "Bourget, Ontario"
    BUSINESS_INSTAGRAM = "https://www.instagram.com/injoy_beautyy"
    
    # Booking settings
    BOOKING_START_HOUR = 15   # 3 PM
    BOOKING_END_HOUR = 20     # 8 PM
    TIME_SLOT_DURATION = 30   # minutes
    
    # Email settings (using Resend - 3,000 free emails/month)
    # Note: API key must be set via RESEND_API_KEY environment variable in Render
    # No default fallback for security - ensures production always uses Render env var
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
    NOTIFICATION_EMAIL = os.environ.get('NOTIFICATION_EMAIL', 'jaymie.injoy.services@gmail.com')  # Receives form notifications
