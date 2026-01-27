"""
Booking routes for Jamie's Beauty Studio.
"""
from flask import Blueprint, request, jsonify
from models import Booking, Service
from email_helper import send_inquiry_notification
from datetime import datetime, timedelta
from config import Config
import re

bookings_bp = Blueprint('bookings', __name__)


def is_valid_email(email):
    """Simple email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@bookings_bp.route('/api/bookings', methods=['POST'])
def create_booking():
    """Create a new booking."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['service_id', 'client_name', 'client_email', 'booking_date', 'booking_time']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate service exists
    service = Service.get_by_id(data['service_id'])
    if not service:
        return jsonify({'error': 'Invalid service selected'}), 400
    
    # Validate date is not in the past
    booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
    if booking_date < datetime.now().date():
        return jsonify({'error': 'Cannot book appointments in the past'}), 400
    
    # Create booking
    try:
        booking_id = Booking.create(
            service_id=data['service_id'],
            client_name=data['client_name'],
            client_email=data['client_email'],
            client_phone=data.get('client_phone', ''),
            booking_date=data['booking_date'],
            booking_time=data['booking_time'],
            notes=data.get('notes', '')
        )
        
        booking = Booking.get_by_id(booking_id)
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Get a specific booking."""
    booking = Booking.get_by_id(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    return jsonify(booking)


@bookings_bp.route('/api/bookings/<int:booking_id>/status', methods=['PATCH'])
def update_booking_status(booking_id):
    """Update booking status."""
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    valid_statuses = ['pending', 'confirmed', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
    
    booking = Booking.get_by_id(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    Booking.update_status(booking_id, data['status'])
    
    return jsonify({'message': 'Booking status updated successfully'})


@bookings_bp.route('/api/available-times', methods=['GET'])
def get_available_times():
    """Get available time slots for a specific date and service."""
    date_str = request.args.get('date')
    service_id = request.args.get('service_id')
    
    if not date_str:
        return jsonify({'error': 'Date is required'}), 400
    
    try:
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Get service duration if provided
    duration = 60  # default duration
    if service_id:
        service = Service.get_by_id(int(service_id))
        if service:
            duration = service['duration']
    
    # Generate all possible time slots
    all_slots = []
    current_time = datetime.strptime(f"{Config.BOOKING_START_HOUR}:00", "%H:%M")
    end_time = datetime.strptime(f"{Config.BOOKING_END_HOUR}:00", "%H:%M")
    
    while current_time < end_time:
        all_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=Config.TIME_SLOT_DURATION)
    
    # Get booked times
    booked = Booking.get_booked_times(date_str)
    
    # Filter out unavailable slots
    available_slots = []
    for slot in all_slots:
        slot_time = datetime.strptime(slot, "%H:%M")
        slot_end = slot_time + timedelta(minutes=duration)
        
        is_available = True
        for booked_time, booked_duration in booked:
            booked_start = datetime.strptime(booked_time, "%H:%M")
            booked_end = booked_start + timedelta(minutes=booked_duration)
            
            # Check for overlap
            if not (slot_end <= booked_start or slot_time >= booked_end):
                is_available = False
                break
        
        # Check if slot doesn't exceed end time
        if slot_end.strftime("%H:%M") > f"{Config.BOOKING_END_HOUR}:00":
            is_available = False
        
        if is_available:
            available_slots.append(slot)
    
    return jsonify({
        'date': date_str,
        'available_times': available_slots
    })


@bookings_bp.route('/api/inquiry', methods=['POST'])
def submit_inquiry():
    """Submit a recurring client inquiry."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['firstName', 'lastName', 'email', 'inquiryType', 'message']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate email format
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    try:
        # Send email notification via Resend
        email_sent = send_inquiry_notification(data)
        
        return jsonify({
            'success': True,
            'message': 'Your inquiry has been sent successfully. Jaymie will get back to you as soon as possible.',
            'email_sent': email_sent
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to send inquiry. Please try again.'
        }), 500
