/**
 * Jamie's Beauty Studio - Booking Functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    const bookingForm = document.getElementById('booking-form');
    const serviceSelect = document.getElementById('service');
    const dateInput = document.getElementById('booking-date');
    const timeSelect = document.getElementById('booking-time');
    const serviceDetails = document.getElementById('service-details');

    // Initialize
    loadServices();
    setupDateInput();
    setupFormHandlers();

    /**
     * Load services into dropdown
     */
    async function loadServices() {
        if (!serviceSelect) return;

        try {
            const services = await api.get('/api/services');
            
            // Group by category
            const grouped = services.reduce((acc, service) => {
                if (!acc[service.category]) {
                    acc[service.category] = [];
                }
                acc[service.category].push(service);
                return acc;
            }, {});

            // Build options
            let html = '<option value="">Select a service...</option>';
            
            for (const [category, categoryServices] of Object.entries(grouped)) {
                html += `<optgroup label="${category}">`;
                categoryServices.forEach(service => {
                    html += `<option value="${service.id}" 
                                data-price="${service.price}" 
                                data-duration="${service.duration}"
                                data-description="${service.description || ''}">
                                ${service.name} - ${utils.formatPrice(service.price)} (${service.duration} min)
                            </option>`;
                });
                html += '</optgroup>';
            }

            serviceSelect.innerHTML = html;
        } catch (error) {
            console.error('Failed to load services:', error);
            serviceSelect.innerHTML = '<option value="">Error loading services</option>';
        }
    }

    /**
     * Setup date input with min date
     */
    function setupDateInput() {
        if (!dateInput) return;

        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        dateInput.min = today;
        dateInput.value = '';

        // Load available times when date changes
        dateInput.addEventListener('change', loadAvailableTimes);
    }

    /**
     * Load available time slots
     */
    async function loadAvailableTimes() {
        if (!timeSelect || !dateInput.value) return;

        const serviceId = serviceSelect.value;
        const date = dateInput.value;

        timeSelect.innerHTML = '<option value="">Loading...</option>';
        timeSelect.disabled = true;

        try {
            let endpoint = `/api/available-times?date=${date}`;
            if (serviceId) {
                endpoint += `&service_id=${serviceId}`;
            }

            const data = await api.get(endpoint);
            
            if (data.available_times.length === 0) {
                timeSelect.innerHTML = '<option value="">No available times</option>';
            } else {
                let html = '<option value="">Select a time...</option>';
                data.available_times.forEach(time => {
                    html += `<option value="${time}">${utils.formatTime(time)}</option>`;
                });
                timeSelect.innerHTML = html;
                timeSelect.disabled = false;
            }
        } catch (error) {
            console.error('Failed to load times:', error);
            timeSelect.innerHTML = '<option value="">Error loading times</option>';
        }
    }

    /**
     * Update service details display
     */
    function updateServiceDetails() {
        if (!serviceDetails || !serviceSelect) return;

        const selected = serviceSelect.selectedOptions[0];
        
        if (!selected || !selected.value) {
            serviceDetails.innerHTML = '';
            return;
        }

        const price = selected.dataset.price;
        const duration = selected.dataset.duration;
        const description = selected.dataset.description;

        serviceDetails.innerHTML = `
            <div class="service-info-card">
                <h4>Service Details</h4>
                <p>${description || 'Professional beauty service tailored to your needs.'}</p>
                <div class="service-meta">
                    <span class="price">${utils.formatPrice(price)}</span>
                    <span class="duration">⏱ ${duration} minutes</span>
                </div>
            </div>
        `;

        // Reload times when service changes (duration affects availability)
        if (dateInput.value) {
            loadAvailableTimes();
        }
    }

    /**
     * Setup form event handlers
     */
    function setupFormHandlers() {
        if (serviceSelect) {
            serviceSelect.addEventListener('change', updateServiceDetails);
        }

        if (bookingForm) {
            bookingForm.addEventListener('submit', handleBookingSubmit);
        }
    }

    /**
     * Handle booking form submission
     */
    async function handleBookingSubmit(e) {
        e.preventDefault();

        const formData = new FormData(bookingForm);
        const submitBtn = bookingForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        // Validate
        if (!formData.get('service') || !formData.get('booking_date') || !formData.get('booking_time')) {
            utils.showAlert(bookingForm, 'Please fill in all required fields.', 'error');
            return;
        }

        if (!utils.validateEmail(formData.get('email'))) {
            utils.showAlert(bookingForm, 'Please enter a valid email address.', 'error');
            return;
        }

        // Show loading state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Booking...';

        try {
            const data = {
                service_id: parseInt(formData.get('service')),
                client_name: formData.get('name'),
                client_email: formData.get('email'),
                client_phone: formData.get('phone') || '',
                booking_date: formData.get('booking_date'),
                booking_time: formData.get('booking_time'),
                notes: formData.get('notes') || ''
            };

            const result = await api.post('/api/bookings', data);

            // Show success
            showBookingConfirmation(result.booking);
            
        } catch (error) {
            utils.showAlert(bookingForm, error.message || 'Failed to create booking. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    }

    /**
     * Show booking confirmation
     */
    function showBookingConfirmation(booking) {
        const formContainer = document.querySelector('.booking-form-container');
        if (!formContainer) return;

        formContainer.innerHTML = `
            <div class="booking-confirmation">
                <div class="confirmation-icon">✓</div>
                <h2>Booking Confirmed!</h2>
                <p>Thank you for booking with Jamie's Beauty Studio.</p>
                
                <div class="confirmation-details">
                    <h3>Appointment Details</h3>
                    <div class="detail-row">
                        <span class="label">Service:</span>
                        <span class="value">${booking.service_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Date:</span>
                        <span class="value">${utils.formatDate(booking.booking_date)}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Time:</span>
                        <span class="value">${utils.formatTime(booking.booking_time)}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Duration:</span>
                        <span class="value">${booking.duration} minutes</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Price:</span>
                        <span class="value">${utils.formatPrice(booking.price)}</span>
                    </div>
                </div>
                
                <p class="confirmation-note">
                    A confirmation email has been sent to <strong>${booking.client_email}</strong>.
                    <br>We'll contact you to confirm your appointment.
                </p>
                
                <div class="confirmation-actions">
                    <a href="index.html" class="btn btn-secondary">Back to Home</a>
                    <a href="booking.html" class="btn btn-primary">Book Another</a>
                </div>
            </div>
        `;
    }
});
