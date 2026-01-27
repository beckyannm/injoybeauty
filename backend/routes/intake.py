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


@intake_bp.route('/api/intake/preview-email', methods=['GET', 'POST'])
def preview_intake_email():
    """Preview what the intake email looks like (for testing)."""
    from email_helper import generate_email_html
    
    # Sample data for preview, or use POST data
    if request.method == 'POST':
        data = request.get_json()
    else:
        # Sample test data
        data = {
            'client_name': 'Jane Test',
            'email': 'jane.test@example.com',
            'phone': '613-555-1234',
            'client_type': 'adult',
            'service_location': 'mobile',
            'address': '123 Test Street, Ottawa, ON',
            'service_requested': 'Haircut and color touch-up. Looking for a trim with some lowlights to blend grays.',
            'hair_length': 'medium',
            'desired_style': 'trim',
            'hair_type': 'wavy',
            'sensitive_to_noise': True,
            'sensitive_to_touch': False,
            'does_not_like_water': True,
            'nervous_anxious': True,
            'enjoys_fidget_toys': True,
            'needs_weighted_cape': False,
            'requires_quiet_environment': True,
            'other_sensory_needs': 'Prefers minimal conversation, likes soft music playing',
            'uses_wheelchair': False,
            'limited_mobility': False,
            'has_behaviours': False,
            'behaviour_notes': '',
            'additional_notes': 'Best contacted via text message. Available weekday afternoons.'
        }
    
    html = generate_email_html(data)
    return html, 200, {'Content-Type': 'text/html'}


@intake_bp.route('/api/intake/test-email', methods=['POST'])
def test_send_email():
    """Send a test email to verify formatting (temporary endpoint)."""
    from email_helper import send_intake_notification
    
    data = request.get_json() or {}
    test_email = data.get('test_email', 'jaymie.injoy.services@gmail.com')
    
    # Sample test data
    test_data = {
        'client_name': 'Test Client',
        'email': 'testclient@example.com',
        'phone': '613-555-1234',
        'client_type': 'adult',
        'service_location': 'mobile',
        'address': '123 Main Street, Bourget, ON',
        'service_requested': 'Looking for a haircut and color touch-up. Would like to blend some grays with lowlights.',
        'hair_length': 'medium',
        'desired_style': 'trim',
        'hair_type': 'wavy',
        'sensitive_to_noise': True,
        'sensitive_to_touch': False,
        'does_not_like_water': True,
        'nervous_anxious': True,
        'enjoys_fidget_toys': True,
        'needs_weighted_cape': False,
        'requires_quiet_environment': True,
        'other_sensory_needs': 'Prefers minimal conversation, likes soft music playing',
        'uses_wheelchair': False,
        'limited_mobility': True,
        'has_behaviours': True,
        'behaviour_notes': 'May get anxious in unfamiliar environments, responds well to calm reassurance',
        'additional_notes': 'Best contacted via text message. Available weekday afternoons after 3pm. Mom will accompany.'
    }
    
    result = send_intake_notification(test_data, override_email=test_email)
    
    if result:
        return jsonify({
            'success': True,
            'message': f'Test email sent to {test_email}!'
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to send email. Make sure RESEND_API_KEY is set as an environment variable in Render.'
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
