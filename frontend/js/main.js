/**
 * Jamie's Beauty Studio - Main JavaScript
 * Core functionality and utilities
 */

// API Base URL
const API_BASE = '';

/**
 * API Helper Functions
 */
const api = {
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    },

    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Request failed');
            return result;
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    },

    async patch(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API PATCH Error:', error);
            throw error;
        }
    }
};

/**
 * Utility Functions
 */
const utils = {
    // Format price with currency
    formatPrice(price) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(price);
    },

    // Format date for display
    formatDate(dateString) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('en-US', options);
    },

    // Format time for display (24h to 12h)
    formatTime(timeString) {
        const [hours, minutes] = timeString.split(':');
        const hour = parseInt(hours);
        const ampm = hour >= 12 ? 'PM' : 'AM';
        const displayHour = hour % 12 || 12;
        return `${displayHour}:${minutes} ${ampm}`;
    },

    // Show alert message
    showAlert(container, message, type = 'success') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        // Remove existing alerts
        const existingAlerts = container.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());
        
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    },

    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Simple form validation
    validateEmail(email) {
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return re.test(email);
    },

    validatePhone(phone) {
        const re = /^[\d\s\-\+\(\)]{10,}$/;
        return re.test(phone);
    }
};

/**
 * Navigation Functionality
 */
function initNavigation() {
    const header = document.querySelector('.header');
    const navToggle = document.querySelector('.nav-toggle');
    const navMobile = document.querySelector('.nav-mobile');
    const navLinks = document.querySelectorAll('.nav-link');

    // Header scroll effect
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // Mobile menu toggle
    if (navToggle && navMobile) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navMobile.classList.toggle('active');
        });

        // Close menu when clicking a link
        navMobile.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navMobile.classList.remove('active');
            });
        });
    }

    // Set active link based on current page
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'index.html')) {
            link.classList.add('active');
        }
    });
}

/**
 * Smooth Scroll for Anchor Links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Intersection Observer for Animations
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    
    if (animatedElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animatedElements.forEach(el => observer.observe(el));
}

/**
 * Load Services Preview (Homepage)
 */
async function loadServicesPreview() {
    const container = document.getElementById('services-preview');
    if (!container) return;

    try {
        const categories = await api.get('/api/services/categories');
        
        const icons = {
            'Hair': '✂',
            'Facial': '◉',
            'Body': '◉',
            'Nailcare': '◈'
        };

        const descriptions = {
            'Hair': 'Precision cuts, stunning color, and beautiful styling for every occasion.',
            'Facial': 'Rejuvenating treatments to reveal your natural glow.',
            'Body': 'Relaxing massages and body treatments for total wellness.',
            'Nailcare': 'Luxurious manicures and pedicures with artistic designs.'
        };

        container.innerHTML = categories.map(cat => `
            <div class="service-card" data-animate>
                <div class="service-icon">${icons[cat] || '💄'}</div>
                <h3>${cat}</h3>
                <p>${descriptions[cat] || 'Professional beauty services tailored to you.'}</p>
                <a href="services.html?category=${cat}" class="btn btn-outline btn-sm">Learn More</a>
            </div>
        `).join('');

        initScrollAnimations();
    } catch (error) {
        console.error('Failed to load services:', error);
    }
}

/**
 * Load Gallery Preview (Homepage)
 */
async function loadGalleryPreview() {
    const container = document.getElementById('gallery-preview');
    if (!container) return;

    try {
        const images = await api.get('/api/gallery/featured');
        
        // Use placeholder images for now
        const placeholderImages = [
            'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=400&h=400&fit=crop'
        ];

        container.innerHTML = images.map((img, index) => `
            <div class="gallery-item">
                <img src="${placeholderImages[index] || placeholderImages[0]}" alt="${img.alt_text || 'Gallery image'}">
                <div class="gallery-overlay">
                    <span>${img.category || 'Portfolio'}</span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load gallery:', error);
        // Show placeholders on error
        const placeholderImages = [
            'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=400&h=400&fit=crop'
        ];
        
        container.innerHTML = placeholderImages.map((src, index) => `
            <div class="gallery-item">
                <img src="${src}" alt="Gallery image ${index + 1}">
                <div class="gallery-overlay">
                    <span>Portfolio</span>
                </div>
            </div>
        `).join('');
    }
}

/**
 * Initialize Everything
 */
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initSmoothScroll();
    initScrollAnimations();
    
    // Load dynamic content if on homepage
    if (document.getElementById('services-preview')) {
        loadServicesPreview();
    }
    if (document.getElementById('gallery-preview')) {
        loadGalleryPreview();
    }
});

// Export for use in other modules
window.api = api;
window.utils = utils;
