"""
Email helper for sending notifications from InJoy Beauty.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config


def send_intake_notification(form_data):
    """
    Send email notification when a new intake form is submitted.
    Returns True if sent, False if email not configured or failed.
    """
    # Check if email is configured
    if not Config.SMTP_PASSWORD:
        print("Email not configured - SMTP_PASSWORD not set. Skipping email notification.")
        return False
    
    try:
        # Build email content
        subject = f"🆕 New Intake Form: {form_data.get('client_name', 'Unknown')}"
        
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
        
        # HTML email body
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #E5C4C4, #D4A5A5); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h1 style="color: #3D3D3D; margin: 0;">✨ New Intake Form Submitted</h1>
            </div>
            
            <div style="background: #FAF8F5; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                <h2 style="color: #D4A5A5; margin-top: 0;">👤 Client Information</h2>
                <p><strong>Name:</strong> {form_data.get('client_name', 'N/A')}</p>
                <p><strong>Email:</strong> {form_data.get('email', 'N/A')}</p>
                <p><strong>Phone:</strong> {form_data.get('phone', 'Not provided')}</p>
                <p><strong>Client Type:</strong> {form_data.get('client_type', 'adult').title()}</p>
            </div>
            
            <div style="background: #FAF8F5; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                <h2 style="color: #D4A5A5; margin-top: 0;">📍 Service Details</h2>
                <p><strong>Location:</strong> {form_data.get('service_location', 'in-salon').replace('-', ' ').title()}</p>
                <p><strong>Address:</strong> {form_data.get('address') or 'N/A (In-salon)'}</p>
                <p><strong>Service Requested:</strong><br>{form_data.get('service_requested', 'Not specified')}</p>
            </div>
            
            <div style="background: #FAF8F5; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                <h2 style="color: #D4A5A5; margin-top: 0;">✂️ Hair Details</h2>
                <p><strong>Current Length:</strong> {(form_data.get('hair_length') or 'Not specified').title()}</p>
                <p><strong>Desired Style:</strong> {(form_data.get('desired_style') or 'Not specified').replace('-', ' ').title()}</p>
                {f"<p><strong>Style Notes:</strong> {form_data.get('desired_style_other')}</p>" if form_data.get('desired_style_other') else ""}
                <p><strong>Hair Type:</strong> {(form_data.get('hair_type') or 'Not specified').title()}</p>
            </div>
            
            <div style="background: #FAF8F5; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                <h2 style="color: #D4A5A5; margin-top: 0;">💜 Sensory & Support Needs</h2>
                {('<ul style="margin: 0; padding-left: 20px;">' + ''.join(f'<li>{need}</li>' for need in sensory_needs) + '</ul>') if sensory_needs else '<p>None selected</p>'}
                {f"<p><strong>Other Sensory Notes:</strong><br>{form_data.get('other_sensory_needs')}</p>" if form_data.get('other_sensory_needs') else ""}
            </div>
            
            <div style="background: #FAF8F5; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                <h2 style="color: #D4A5A5; margin-top: 0;">♿ Mobility & Safety</h2>
                {('<ul style="margin: 0; padding-left: 20px;">' + ''.join(f'<li>{need}</li>' for need in mobility_needs) + '</ul>') if mobility_needs else '<p>None selected</p>'}
                {f"<p><strong>Behaviour Notes:</strong><br>{form_data.get('behaviour_notes')}</p>" if form_data.get('behaviour_notes') else ""}
            </div>
            
            {f'''<div style="background: #FAF8F5; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                <h2 style="color: #D4A5A5; margin-top: 0;">📝 Additional Notes</h2>
                <p>{form_data.get('additional_notes')}</p>
            </div>''' if form_data.get('additional_notes') else ""}
            
            <div style="text-align: center; padding: 20px; color: #6B6B6B;">
                <p>This form was submitted through the InJoy Beauty website.</p>
                <p><a href="mailto:{form_data.get('email')}" style="color: #D4A5A5;">Reply to {form_data.get('client_name')}</a></p>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        text_body = f"""
New Intake Form Submitted

CLIENT INFORMATION
Name: {form_data.get('client_name', 'N/A')}
Email: {form_data.get('email', 'N/A')}
Phone: {form_data.get('phone', 'Not provided')}
Client Type: {form_data.get('client_type', 'adult').title()}

SERVICE DETAILS
Location: {form_data.get('service_location', 'in-salon')}
Address: {form_data.get('address') or 'N/A (In-salon)'}
Service Requested: {form_data.get('service_requested', 'Not specified')}

HAIR DETAILS
Current Length: {form_data.get('hair_length') or 'Not specified'}
Desired Style: {form_data.get('desired_style') or 'Not specified'}
Hair Type: {form_data.get('hair_type') or 'Not specified'}

SENSORY & SUPPORT NEEDS
{chr(10).join(f'- {need}' for need in sensory_needs) if sensory_needs else 'None selected'}
{f"Other Notes: {form_data.get('other_sensory_needs')}" if form_data.get('other_sensory_needs') else ""}

MOBILITY & SAFETY
{chr(10).join(f'- {need}' for need in mobility_needs) if mobility_needs else 'None selected'}
{f"Behaviour Notes: {form_data.get('behaviour_notes')}" if form_data.get('behaviour_notes') else ""}

{f"ADDITIONAL NOTES{chr(10)}{form_data.get('additional_notes')}" if form_data.get('additional_notes') else ""}

---
This form was submitted through the InJoy Beauty website.
        """
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = Config.SMTP_EMAIL
        msg['To'] = Config.NOTIFICATION_EMAIL
        msg['Reply-To'] = form_data.get('email', Config.SMTP_EMAIL)
        
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"Email notification sent to {Config.NOTIFICATION_EMAIL}")
        return True
        
    except Exception as e:
        print(f"Failed to send email notification: {e}")
        return False
