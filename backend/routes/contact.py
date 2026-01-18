"""
Contact routes for Jamie's Beauty Studio.
"""
from flask import Blueprint, request, jsonify
from models import ContactMessage
import re

contact_bp = Blueprint('contact', __name__)


def is_valid_email(email):
    """Simple email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@contact_bp.route('/api/contact', methods=['POST'])
def submit_contact():
    """Submit a contact message."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'message']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate email format
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Create message
    try:
        message_id = ContactMessage.create(
            name=data['name'].strip(),
            email=data['email'].strip(),
            subject=data.get('subject', '').strip(),
            message=data['message'].strip()
        )
        
        return jsonify({
            'message': 'Your message has been sent successfully. We will get back to you soon!',
            'id': message_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to send message. Please try again.'}), 500


@contact_bp.route('/api/contact/messages', methods=['GET'])
def get_messages():
    """Get all contact messages (admin endpoint)."""
    # In production, this should be protected with authentication
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    messages = ContactMessage.get_all(unread_only=unread_only)
    return jsonify(messages)


@contact_bp.route('/api/contact/messages/<int:message_id>/read', methods=['PATCH'])
def mark_read(message_id):
    """Mark a message as read."""
    ContactMessage.mark_as_read(message_id)
    return jsonify({'message': 'Message marked as read'})
