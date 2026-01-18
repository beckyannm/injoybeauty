# Jamie's Beauty Studio - Project Plan

## Overview

A modern, elegant website for Jamie's Beauty Studio - a mobile beauty services business offering hair, facial, body, and nail care services. The website will feature online booking capabilities, a portfolio gallery, and contact functionality.

---

## 🎯 Project Goals

1. **Establish Online Presence** - Create a professional, visually appealing website that reflects the quality of Jamie's services
2. **Enable Online Bookings** - Allow clients to easily book appointments for various services
3. **Showcase Work** - Display a portfolio gallery with editorial-style photos
4. **Provide Information** - Share details about Jamie, services offered, and contact information

---

## 📋 Requirements

### Functional Requirements

| Feature | Description |
|---------|-------------|
| **Home Page** | Landing page with hero section, featured services, and call-to-action |
| **About Page** | Jamie's story, qualifications, and philosophy |
| **Services Page** | Detailed list of all services (Hair, Facial, Body, Nailcare) with descriptions and pricing |
| **Booking System** | Interactive booking form with date/time selection and service selection |
| **Gallery** | Editorial-style portfolio with masonry/grid layout |
| **Contact Page** | Contact form, location info (mobile service areas), and social links |

### Non-Functional Requirements

- **Responsive Design** - Mobile-first approach, works on all devices
- **Performance** - Fast load times, optimized images
- **Accessibility** - WCAG 2.1 AA compliance
- **SEO** - Basic SEO optimization

---

## 🎨 Design System

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Cream | `#F5F0E8` | Primary background |
| Soft Beige | `#E8DFD5` | Secondary background |
| Warm Taupe | `#C4B7A6` | Borders, subtle accents |
| Dusty Rose | `#D4A5A5` | Primary accent |
| Sage | `#B5C4B1` | Secondary accent |
| Charcoal | `#3D3D3D` | Primary text |
| Soft Gray | `#6B6B6B` | Secondary text |

### Typography

- **Headings**: Elegant serif font (e.g., Cormorant Garamond, Playfair Display)
- **Body**: Clean sans-serif (e.g., Lato, Source Sans Pro)

### Design Style

- Neutral pastels and earth tones
- Clean, minimalist aesthetic
- Editorial/magazine-style imagery
- Generous whitespace
- Subtle animations and transitions

---

## 🛠 Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python (Flask) |
| **Database** | SQLite |
| **Hosting** | TBD |

---

## 📁 Project Structure

```
becky-project/
├── backend/
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database initialization and helpers
│   ├── models.py           # SQLite models/schema
│   └── routes/
│       ├── __init__.py
│       ├── bookings.py     # Booking endpoints
│       ├── contact.py      # Contact form endpoint
│       └── gallery.py      # Gallery endpoints
├── frontend/
│   ├── index.html          # Home page
│   ├── about.html          # About Jamie
│   ├── services.html       # Services listing
│   ├── booking.html        # Booking page
│   ├── gallery.html        # Portfolio gallery
│   ├── contact.html        # Contact page
│   ├── css/
│   │   ├── styles.css      # Main stylesheet
│   │   ├── variables.css   # CSS custom properties
│   │   └── components.css  # Reusable components
│   ├── js/
│   │   ├── main.js         # Main JavaScript
│   │   ├── booking.js      # Booking functionality
│   │   ├── gallery.js      # Gallery interactions
│   │   └── navigation.js   # Navigation/menu
│   └── assets/
│       ├── images/
│       │   ├── hero/       # Hero images
│       │   ├── gallery/    # Portfolio images
│       │   ├── about/      # About page images
│       │   └── icons/      # Icons and logos
│       └── fonts/          # Custom fonts (if any)
├── database/
│   └── salon.db            # SQLite database file
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
├── PROJECT_PLAN.md        # This file
└── README.md              # Project readme
```

---

## 📊 Database Schema

### Tables

#### `services`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| category | TEXT | Hair, Facial, Body, Nailcare |
| name | TEXT | Service name |
| description | TEXT | Service description |
| duration | INTEGER | Duration in minutes |
| price | REAL | Price |
| is_active | BOOLEAN | Available for booking |

#### `bookings`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| service_id | INTEGER | Foreign key to services |
| client_name | TEXT | Client's name |
| client_email | TEXT | Client's email |
| client_phone | TEXT | Client's phone |
| booking_date | DATE | Appointment date |
| booking_time | TIME | Appointment time |
| notes | TEXT | Special requests |
| status | TEXT | pending/confirmed/cancelled |
| created_at | DATETIME | Record creation timestamp |

#### `contact_messages`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Sender's name |
| email | TEXT | Sender's email |
| subject | TEXT | Message subject |
| message | TEXT | Message content |
| created_at | DATETIME | Timestamp |
| is_read | BOOLEAN | Read status |

#### `gallery_images`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| filename | TEXT | Image filename |
| alt_text | TEXT | Accessibility text |
| category | TEXT | Category tag |
| is_featured | BOOLEAN | Featured on homepage |
| sort_order | INTEGER | Display order |
| created_at | DATETIME | Upload timestamp |

---

## 📄 Pages Breakdown

### 1. Home Page (`index.html`)
- Hero section with tagline and CTA
- Featured services preview
- About teaser
- Gallery preview (3-4 featured images)
- Testimonials section
- Footer with contact info

### 2. About Page (`about.html`)
- Jamie's story and background
- Professional photo
- Qualifications and training
- Philosophy/approach to beauty
- Personal touch elements

### 3. Services Page (`services.html`)
- Service categories with icons
- Detailed service listings
- Pricing information
- Duration estimates
- Book now buttons

### 4. Booking Page (`booking.html`)
- Service selection dropdown
- Calendar date picker
- Time slot selection
- Client information form
- Confirmation system

### 5. Gallery Page (`gallery.html`)
- Masonry/grid layout
- Category filters
- Lightbox for full-size viewing
- Editorial-style presentation

### 6. Contact Page (`contact.html`)
- Contact form
- Phone and email
- Service areas (mobile business)
- Social media links
- Operating hours

---

## 🚀 Development Phases

### Phase 1: Foundation (Current)
- [x] Create project plan
- [ ] Set up folder structure
- [ ] Initialize Git repository
- [ ] Create basic HTML templates
- [ ] Set up CSS framework

### Phase 2: Frontend Development
- [ ] Design and implement all pages
- [ ] Create responsive layouts
- [ ] Add animations and interactions
- [ ] Implement gallery lightbox
- [ ] Build booking form UI

### Phase 3: Backend Development
- [ ] Set up Flask application
- [ ] Create database schema
- [ ] Implement booking API
- [ ] Create contact form handler
- [ ] Build admin functionality (optional)

### Phase 4: Integration
- [ ] Connect frontend to backend
- [ ] Test booking flow
- [ ] Test contact form
- [ ] Add form validation

### Phase 5: Polish & Launch
- [ ] Add placeholder images
- [ ] Performance optimization
- [ ] Cross-browser testing
- [ ] Mobile testing
- [ ] Final review

---

## 📝 Notes

- **Mobile Services**: Jamie offers mobile beauty services, so the location/address section should emphasize service areas rather than a physical location
- **Placeholder Images**: Use high-quality editorial placeholder images that can be replaced with actual photos later
- **Scalability**: Design the booking system to be easily expandable for future features like online payments

---

*Last Updated: January 17, 2026*
