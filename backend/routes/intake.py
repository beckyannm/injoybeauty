"""
Intake form routes for InJoy Beauty.
"""
from flask import Blueprint, request, jsonify
import sys
sys.path.insert(0, '..')
from models import IntakeForm
from email_helper import send_intake_notification

intake_bp = Blueprint('intake', __name__)


@intake_bp.route('/api/intake', methods=['POST'])
def submit_intake_form():
    """Submit a new client intake form."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['client_name', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create the intake form in database
        form_id = IntakeForm.create(data)
        
        # Send email notification to Jaymie
        email_sent = send_intake_notification(data)
        
        return jsonify({
            'success': True,
            'message': 'Intake form submitted successfully! Jaymie will review your information and contact you soon.',
            'form_id': form_id,
            'email_sent': email_sent
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@intake_bp.route('/api/intake', methods=['GET'])
def get_intake_forms():
    """Get all intake forms (admin)."""
    try:
        status = request.args.get('status')
        forms = IntakeForm.get_all(status=status)
        
        return jsonify({
            'success': True,
            'forms': forms,
            'count': len(forms)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@intake_bp.route('/api/intake/<int:form_id>', methods=['GET'])
def get_intake_form(form_id):
    """Get a single intake form by ID."""
    try:
        form = IntakeForm.get_by_id(form_id)
        
        if not form:
            return jsonify({
                'success': False,
                'error': 'Intake form not found'
            }), 404
        
        return jsonify({
            'success': True,
            'form': form
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@intake_bp.route('/api/intake/<int:form_id>/status', methods=['PATCH'])
def update_intake_status(form_id):
    """Update the status of an intake form."""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({
                'success': False,
                'error': 'Status is required'
            }), 400
        
        valid_statuses = ['new', 'reviewed', 'contacted', 'scheduled', 'completed', 'archived']
        if status not in valid_statuses:
            return jsonify({
                'success': False,
                'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }), 400
        
        IntakeForm.update_status(form_id, status)
        
        return jsonify({
            'success': True,
            'message': f'Status updated to {status}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
