"""
Email helper for sending notifications from InJoy Beauty.
Uses Resend for reliable email delivery.
"""
import resend
from config import Config

# Initialize Resend
resend.api_key = Config.RESEND_API_KEY


def generate_email_html(form_data):
    """Generate HTML email content for intake form."""
    # Build sensory needs list
    sensory_needs = []
    if form_data.get('sensitive_to_noise'):
        sensory_needs.append("Sensitive to loud noise")
    if form_data.get('sensitive_to_touch'):
        sensory_needs.append("Sensitive to touch")
    if form_data.get('does_not_like_water'):
        sensory_needs.append("Does not like water")
    if form_data.get('nervous_anxious'):
        sensory_needs.append("Nervous/anxious during appointments")
    if form_data.get('enjoys_fidget_toys'):
        sensory_needs.append("Enjoys fidget toys")
    if form_data.get('needs_weighted_cape'):
        sensory_needs.append("Would benefit from weighted cape")
    if form_data.get('requires_quiet_environment'):
        sensory_needs.append("Requires quiet/low-sensory environment")
    
    # Build mobility list
    mobility_needs = []
    if form_data.get('uses_wheelchair'):
        mobility_needs.append("Uses wheelchair")
    if form_data.get('limited_mobility'):
        mobility_needs.append("Limited mobility")
    if form_data.get('has_behaviours'):
        mobility_needs.append("May have behaviours (see notes)")
    
    # HTML email body - clean headers without emojis for better compatibility
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #F5F0E8;">
        <div style="background: linear-gradient(135deg, #E5C4C4, #D4A5A5); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h1 style="color: #3D3D3D; margin: 0; font-size: 24px;">New Intake Form Submitted</h1>
            <p style="color: #4A4A4A; margin: 10px 0 0 0;">InJoy Beauty - Inclusive Beauty Services</p>
        </div>
        
        <div style="background: #FFFFFF; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #D4A5A5;">
            <h2 style="color: #D4A5A5; margin-top: 0; font-size: 18px;">Client Information</h2>
            <p><strong>Name:</strong> {form_data.get('client_name', 'N/A')}</p>
            <p><strong>Email:</strong> <a href="mailto:{form_data.get('email', '')}">{form_data.get('email', 'N/A')}</a></p>
            <p><strong>Phone:</strong> <a href="tel:{form_data.get('phone', '')}">{form_data.get('phone', 'Not provided')}</a></p>
            <p><strong>Client Type:</strong> {form_data.get('client_type', 'adult').title()}</p>
        </div>
        
        <div style="background: #FFFFFF; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #D4A5A5;">
            <h2 style="color: #D4A5A5; margin-top: 0; font-size: 18px;">Service Details</h2>
            <p><strong>Location:</strong> {form_data.get('service_location', 'in-salon').replace('-', ' ').title()}</p>
            <p><strong>Address:</strong> {form_data.get('address') or 'N/A (In-salon)'}</p>
            <p><strong>Service Requested:</strong></p>
            <p style="background: #FAF8F5; padding: 10px; border-radius: 5px; margin-top: 5px;">{form_data.get('service_requested', 'Not specified')}</p>
        </div>
        
        <div style="background: #FFFFFF; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #D4A5A5;">
            <h2 style="color: #D4A5A5; margin-top: 0; font-size: 18px;">Hair Details</h2>
            <p><strong>Current Length:</strong> {(form_data.get('hair_length') or 'Not specified').title()}</p>
            <p><strong>Desired Style:</strong> {(form_data.get('desired_style') or 'Not specified').replace('-', ' ').title()}</p>
            {f"<p><strong>Style Notes:</strong> {form_data.get('desired_style_other')}</p>" if form_data.get('desired_style_other') else ""}
            <p><strong>Hair Type:</strong> {(form_data.get('hair_type') or 'Not specified').title()}</p>
        </div>
        
        <div style="background: #FFFFFF; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #9B59B6;">
            <h2 style="color: #9B59B6; margin-top: 0; font-size: 18px;">Sensory & Support Needs</h2>
            {('<ul style="margin: 0; padding-left: 20px;">' + ''.join(f'<li style="margin-bottom: 5px;">{need}</li>' for need in sensory_needs) + '</ul>') if sensory_needs else '<p style="color: #888;">None selected</p>'}
            {f"<p style='margin-top: 15px;'><strong>Other Sensory Notes:</strong></p><p style='background: #FAF8F5; padding: 10px; border-radius: 5px;'>{form_data.get('other_sensory_needs')}</p>" if form_data.get('other_sensory_needs') else ""}
        </div>
        
        <div style="background: #FFFFFF; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #3498DB;">
            <h2 style="color: #3498DB; margin-top: 0; font-size: 18px;">Mobility & Safety</h2>
            {('<ul style="margin: 0; padding-left: 20px;">' + ''.join(f'<li style="margin-bottom: 5px;">{need}</li>' for need in mobility_needs) + '</ul>') if mobility_needs else '<p style="color: #888;">None selected</p>'}
            {f"<p style='margin-top: 15px;'><strong>Behaviour Notes:</strong></p><p style='background: #FFF3CD; padding: 10px; border-radius: 5px; border: 1px solid #FFE69C;'>{form_data.get('behaviour_notes')}</p>" if form_data.get('behaviour_notes') else ""}
        </div>
        
        {f'''<div style="background: #FFFFFF; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #27AE60;">
            <h2 style="color: #27AE60; margin-top: 0; font-size: 18px;">Additional Notes</h2>
            <p style="background: #FAF8F5; padding: 10px; border-radius: 5px;">{form_data.get('additional_notes')}</p>
        </div>''' if form_data.get('additional_notes') else ""}
        
        <div style="text-align: center; padding: 20px; color: #6B6B6B; border-top: 2px solid #E8DFD5; margin-top: 20px;">
            <p style="margin-bottom: 15px;">This form was submitted through the <strong>InJoy Beauty</strong> website.</p>
            <a href="mailto:{form_data.get('email')}" style="display: inline-block; background: #D4A5A5; color: white; padding: 12px 25px; border-radius: 25px; text-decoration: none; font-weight: bold;">Reply to {form_data.get('client_name')}</a>
        </div>
    </body>
    </html>
    """
    return html_body


def send_intake_notification(form_data, override_email=None):
    """
    Send email notification when a new intake form is submitted.
    Returns True if sent, False if failed.
    
    Args:
        form_data: Dictionary containing the form submission data
        override_email: Optional email address to send to instead of the default
    """
    if not Config.RESEND_API_KEY:
        print("Email not configured - RESEND_API_KEY not set.")
        return False
    
    try:
        recipient = override_email or Config.NOTIFICATION_EMAIL
        subject = f"New Intake Form: {form_data.get('client_name', 'Unknown Client')}"
        html_body = generate_email_html(form_data)
        
        # Send via Resend
        params = {
            "from": "InJoy Beauty <onboarding@resend.dev>",
            "to": [recipient],
            "subject": subject,
            "html": html_body,
            "reply_to": form_data.get('email')
        }
        
        response = resend.Emails.send(params)
        print(f"Email sent successfully to {recipient}! ID: {response.get('id')}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
