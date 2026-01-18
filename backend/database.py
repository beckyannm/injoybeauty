"""
Database initialization and helper functions for Jamie's Beauty Studio.
"""
import sqlite3
from pathlib import Path
from config import DATABASE_PATH


def get_db_connection():
    """Create and return a database connection."""
    # Ensure the database directory exists
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def init_db():
    """Initialize the database with all required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create services table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            duration INTEGER NOT NULL,
            price REAL NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id INTEGER NOT NULL,
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL,
            client_phone TEXT,
            booking_date DATE NOT NULL,
            booking_time TIME NOT NULL,
            notes TEXT,
            status TEXT DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    ''')
    
    # Create contact_messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_read BOOLEAN DEFAULT 0
        )
    ''')
    
    # Create gallery_images table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            alt_text TEXT,
            category TEXT,
            is_featured BOOLEAN DEFAULT 0,
            sort_order INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def seed_services():
    """Seed the database with initial services."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if services already exist
    cursor.execute('SELECT COUNT(*) FROM services')
    if cursor.fetchone()[0] > 0:
        print("Services already seeded.")
        conn.close()
        return
    
    services = [
        # Hair Services
        ('Hair', 'Haircut & Style', 'Precision cut tailored to your face shape and lifestyle, finished with a beautiful style.', 60, 75.00),
        ('Hair', 'Blowout', 'Professional blow dry and styling for any occasion.', 45, 55.00),
        ('Hair', 'Color - Full', 'Full head color application with premium products.', 120, 150.00),
        ('Hair', 'Color - Highlights', 'Dimensional highlights or lowlights for added depth.', 150, 180.00),
        ('Hair', 'Balayage', 'Hand-painted highlights for a natural, sun-kissed look.', 180, 220.00),
        ('Hair', 'Deep Conditioning Treatment', 'Intensive moisture treatment for damaged or dry hair.', 30, 45.00),
        
        # Facial Services
        ('Facial', 'Classic Facial', 'Deep cleansing facial with extraction and hydration.', 60, 85.00),
        ('Facial', 'Anti-Aging Facial', 'Targeted treatment to reduce fine lines and restore radiance.', 75, 120.00),
        ('Facial', 'Hydrating Facial', 'Intensive moisture boost for dehydrated skin.', 60, 95.00),
        ('Facial', 'Acne Treatment Facial', 'Specialized treatment for acne-prone skin.', 60, 90.00),
        
        # Body Services
        ('Body', 'Full Body Massage', 'Relaxing Swedish massage to release tension.', 60, 95.00),
        ('Body', 'Deep Tissue Massage', 'Targeted pressure to relieve chronic muscle tension.', 60, 110.00),
        ('Body', 'Body Scrub & Wrap', 'Exfoliation followed by a nourishing body wrap.', 90, 130.00),
        ('Body', 'Back Facial', 'Deep cleansing and treatment for the back area.', 45, 75.00),
        
        # Nail Services
        ('Nailcare', 'Classic Manicure', 'Nail shaping, cuticle care, and polish application.', 30, 35.00),
        ('Nailcare', 'Gel Manicure', 'Long-lasting gel polish manicure.', 45, 50.00),
        ('Nailcare', 'Classic Pedicure', 'Relaxing foot treatment with polish.', 45, 45.00),
        ('Nailcare', 'Spa Pedicure', 'Luxurious pedicure with extended massage and mask.', 60, 65.00),
        ('Nailcare', 'Nail Art', 'Custom nail art designs (per nail).', 15, 10.00),
    ]
    
    cursor.executemany('''
        INSERT INTO services (category, name, description, duration, price)
        VALUES (?, ?, ?, ?, ?)
    ''', services)
    
    conn.commit()
    conn.close()
    print(f"Seeded {len(services)} services successfully!")


def seed_gallery():
    """Seed the database with placeholder gallery images."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if gallery already has images
    cursor.execute('SELECT COUNT(*) FROM gallery_images')
    if cursor.fetchone()[0] > 0:
        print("Gallery already seeded.")
        conn.close()
        return
    
    images = [
        ('gallery-1.jpg', 'Elegant updo hairstyle', 'Hair', 1, 1),
        ('gallery-2.jpg', 'Natural balayage highlights', 'Hair', 1, 2),
        ('gallery-3.jpg', 'Bridal makeup and hair', 'Hair', 0, 3),
        ('gallery-4.jpg', 'Relaxing facial treatment', 'Facial', 1, 4),
        ('gallery-5.jpg', 'Glowing skin after facial', 'Facial', 0, 5),
        ('gallery-6.jpg', 'Artistic nail design', 'Nailcare', 1, 6),
        ('gallery-7.jpg', 'French tip manicure', 'Nailcare', 0, 7),
        ('gallery-8.jpg', 'Spa pedicure treatment', 'Nailcare', 0, 8),
        ('gallery-9.jpg', 'Studio interior', 'Studio', 0, 9),
        ('gallery-10.jpg', 'Product display', 'Studio', 0, 10),
        ('gallery-11.jpg', 'Color transformation', 'Hair', 0, 11),
        ('gallery-12.jpg', 'Massage therapy session', 'Body', 0, 12),
    ]
    
    cursor.executemany('''
        INSERT INTO gallery_images (filename, alt_text, category, is_featured, sort_order)
        VALUES (?, ?, ?, ?, ?)
    ''', images)
    
    conn.commit()
    conn.close()
    print(f"Seeded {len(images)} gallery images successfully!")


if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("\nSeeding services...")
    seed_services()
    print("\nSeeding gallery...")
    seed_gallery()
    print("\nDatabase setup complete!")
