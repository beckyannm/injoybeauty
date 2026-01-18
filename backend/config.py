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
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
    
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
    
    # Email settings (for notifications)
    # To enable email: set SMTP_PASSWORD environment variable with Gmail App Password
    # Get App Password: Google Account > Security > 2-Step Verification > App passwords
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_EMAIL = os.environ.get('SMTP_EMAIL', 'jaymie.injoy.services@gmail.com')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')  # Gmail App Password
    NOTIFICATION_EMAIL = os.environ.get('NOTIFICATION_EMAIL', 'jaymie.injoy.services@gmail.com')
