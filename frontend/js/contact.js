/**
 * Jamie's Beauty Studio - Contact Form Functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
    }

    /**
     * Handle contact form submission
     */
    async function handleContactSubmit(e) {
        e.preventDefault();

        const formData = new FormData(contactForm);
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        // Validate required fields
        const name = formData.get('name')?.trim();
        const email = formData.get('email')?.trim();
        const message = formData.get('message')?.trim();

        if (!name || !email || !message) {
            utils.showAlert(contactForm, 'Please fill in all required fields.', 'error');
            return;
        }

        if (!utils.validateEmail(email)) {
            utils.showAlert(contactForm, 'Please enter a valid email address.', 'error');
            return;
        }

        // Show loading state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        try {
            const data = {
                name: name,
                email: email,
                subject: formData.get('subject')?.trim() || '',
                message: message
            };

            const result = await api.post('/api/contact', data);

            // Show success
            showSuccessMessage(result.message);
            contactForm.reset();
            
        } catch (error) {
            utils.showAlert(contactForm, error.message || 'Failed to send message. Please try again.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    }

    /**
     * Show success message
     */
    function showSuccessMessage(message) {
        const formContainer = contactForm.parentElement;
        
        const successDiv = document.createElement('div');
        successDiv.className = 'contact-success';
        successDiv.innerHTML = `
            <div class="success-icon">✓</div>
            <h3>Message Sent!</h3>
            <p>${message}</p>
            <button class="btn btn-secondary" onclick="this.parentElement.remove()">Send Another Message</button>
        `;

        // Hide form temporarily
        contactForm.style.display = 'none';
        formContainer.appendChild(successDiv);

        // Show form again after clicking the button
        successDiv.querySelector('button').addEventListener('click', () => {
            successDiv.remove();
            contactForm.style.display = 'block';
        });
    }
});
