"""
Configuration settings for Jamie's Beauty Studio backend.
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
    BUSINESS_NAME = "Jamie's Beauty Studio"
    BUSINESS_EMAIL = "hello@jamiesbeauty.com"
    BUSINESS_PHONE = "(555) 123-4567"
    
    # Booking settings
    BOOKING_START_HOUR = 9   # 9 AM
    BOOKING_END_HOUR = 18    # 6 PM
    TIME_SLOT_DURATION = 30  # minutes
