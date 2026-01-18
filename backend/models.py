"""
Data models and database query helpers for Jamie's Beauty Studio.
"""
from database import get_db_connection
from datetime import datetime, date


class Service:
    """Service model for beauty services."""
    
    @staticmethod
    def get_all(active_only=True):
        """Get all services, optionally filtered by active status."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute('SELECT * FROM services WHERE is_active = 1 ORDER BY category, name')
        else:
            cursor.execute('SELECT * FROM services ORDER BY category, name')
        
        services = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return services
    
    @staticmethod
    def get_by_id(service_id):
        """Get a single service by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM services WHERE id = ?', (service_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def get_by_category(category):
        """Get all services in a category."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM services WHERE category = ? AND is_active = 1 ORDER BY name',
            (category,)
        )
        services = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return services
    
    @staticmethod
    def get_categories():
        """Get list of unique service categories."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT category FROM services WHERE is_active = 1 ORDER BY category')
        categories = [row['category'] for row in cursor.fetchall()]
        conn.close()
        return categories


class Booking:
    """Booking model for appointments."""
    
    @staticmethod
    def create(service_id, client_name, client_email, client_phone, booking_date, booking_time, notes=None):
        """Create a new booking."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO bookings (service_id, client_name, client_email, client_phone, booking_date, booking_time, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (service_id, client_name, client_email, client_phone, booking_date, booking_time, notes))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return booking_id
    
    @staticmethod
    def get_by_id(booking_id):
        """Get a booking by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, s.name as service_name, s.duration, s.price
            FROM bookings b
            JOIN services s ON b.service_id = s.id
            WHERE b.id = ?
        ''', (booking_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def get_by_date(booking_date):
        """Get all bookings for a specific date."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, s.name as service_name, s.duration
            FROM bookings b
            JOIN services s ON b.service_id = s.id
            WHERE b.booking_date = ? AND b.status != 'cancelled'
            ORDER BY b.booking_time
        ''', (booking_date,))
        bookings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return bookings
    
    @staticmethod
    def update_status(booking_id, status):
        """Update booking status."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE bookings SET status = ? WHERE id = ?',
            (status, booking_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_booked_times(booking_date):
        """Get list of booked time slots for a date."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT booking_time, s.duration
            FROM bookings b
            JOIN services s ON b.service_id = s.id
            WHERE booking_date = ? AND status != 'cancelled'
        ''', (booking_date,))
        bookings = cursor.fetchall()
        conn.close()
        return [(row['booking_time'], row['duration']) for row in bookings]


class ContactMessage:
    """Contact message model."""
    
    @staticmethod
    def create(name, email, subject, message):
        """Create a new contact message."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contact_messages (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        ''', (name, email, subject, message))
        
        message_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return message_id
    
    @staticmethod
    def get_all(unread_only=False):
        """Get all contact messages."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if unread_only:
            cursor.execute('SELECT * FROM contact_messages WHERE is_read = 0 ORDER BY created_at DESC')
        else:
            cursor.execute('SELECT * FROM contact_messages ORDER BY created_at DESC')
        
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return messages
    
    @staticmethod
    def mark_as_read(message_id):
        """Mark a message as read."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE contact_messages SET is_read = 1 WHERE id = ?', (message_id,))
        conn.commit()
        conn.close()


class GalleryImage:
    """Gallery image model."""
    
    @staticmethod
    def get_all():
        """Get all gallery images."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM gallery_images ORDER BY sort_order')
        images = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return images
    
    @staticmethod
    def get_featured():
        """Get featured gallery images."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM gallery_images WHERE is_featured = 1 ORDER BY sort_order LIMIT 4')
        images = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return images
    
    @staticmethod
    def get_by_category(category):
        """Get gallery images by category."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM gallery_images WHERE category = ? ORDER BY sort_order',
            (category,)
        )
        images = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return images


class IntakeForm:
    """Client intake form model for InJoy Beauty."""
    
    @staticmethod
    def create(data):
        """Create a new intake form submission."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO intake_forms (
                client_name, phone, email, client_type,
                service_location, address, service_requested,
                hair_length, desired_style, desired_style_other, hair_type,
                sensitive_to_noise, sensitive_to_touch, does_not_like_water,
                nervous_anxious, enjoys_fidget_toys, needs_weighted_cape,
                requires_quiet_environment, other_sensory_needs,
                uses_wheelchair, limited_mobility, has_behaviours, behaviour_notes,
                additional_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('client_name'),
            data.get('phone'),
            data.get('email'),
            data.get('client_type', 'adult'),
            data.get('service_location', 'in-salon'),
            data.get('address'),
            data.get('service_requested'),
            data.get('hair_length'),
            data.get('desired_style'),
            data.get('desired_style_other'),
            data.get('hair_type'),
            1 if data.get('sensitive_to_noise') else 0,
            1 if data.get('sensitive_to_touch') else 0,
            1 if data.get('does_not_like_water') else 0,
            1 if data.get('nervous_anxious') else 0,
            1 if data.get('enjoys_fidget_toys') else 0,
            1 if data.get('needs_weighted_cape') else 0,
            1 if data.get('requires_quiet_environment') else 0,
            data.get('other_sensory_needs'),
            1 if data.get('uses_wheelchair') else 0,
            1 if data.get('limited_mobility') else 0,
            1 if data.get('has_behaviours') else 0,
            data.get('behaviour_notes'),
            data.get('additional_notes')
        ))
        
        form_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return form_id
    
    @staticmethod
    def get_all(status=None):
        """Get all intake forms, optionally filtered by status."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute('SELECT * FROM intake_forms WHERE status = ? ORDER BY created_at DESC', (status,))
        else:
            cursor.execute('SELECT * FROM intake_forms ORDER BY created_at DESC')
        
        forms = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return forms
    
    @staticmethod
    def get_by_id(form_id):
        """Get a single intake form by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM intake_forms WHERE id = ?', (form_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def update_status(form_id, status):
        """Update the status of an intake form."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE intake_forms SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (status, form_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_by_email(email):
        """Get all intake forms for a specific email."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM intake_forms WHERE email = ? ORDER BY created_at DESC', (email,))
        forms = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return forms
