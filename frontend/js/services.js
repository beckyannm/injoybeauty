/**
 * Jamie's Beauty Studio - Services Page Functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    const servicesContainer = document.getElementById('services-container');
    const categoryTabs = document.querySelectorAll('.category-tab');
    
    let allServices = [];
    let currentCategory = 'all';

    // Check URL params for category
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category');
    if (categoryParam) {
        currentCategory = categoryParam;
    }

    // Initialize
    loadServices();
    setupCategoryTabs();

    /**
     * Load all services
     */
    async function loadServices() {
        if (!servicesContainer) return;

        servicesContainer.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading services...</p></div>';

        try {
            allServices = await api.get('/api/services');
            
            if (currentCategory !== 'all') {
                // Set active tab for URL param
                categoryTabs.forEach(tab => {
                    tab.classList.toggle('active', tab.dataset.category === currentCategory);
                });
            }
            
            renderServices();
        } catch (error) {
            console.error('Failed to load services:', error);
            servicesContainer.innerHTML = `
                <div class="error-message">
                    <p>Unable to load services. Please try again later.</p>
                    <button class="btn btn-secondary" onclick="location.reload()">Retry</button>
                </div>
            `;
        }
    }

    /**
     * Render services by category
     */
    function renderServices() {
        if (!servicesContainer) return;

        const filteredServices = currentCategory === 'all' 
            ? allServices 
            : allServices.filter(s => s.category === currentCategory);

        if (filteredServices.length === 0) {
            servicesContainer.innerHTML = '<p class="no-services">No services found in this category.</p>';
            return;
        }

        // Group by category
        const grouped = filteredServices.reduce((acc, service) => {
            if (!acc[service.category]) {
                acc[service.category] = [];
            }
            acc[service.category].push(service);
            return acc;
        }, {});

        const categoryIcons = {
            'Hair': '✂️',
            'Facial': '✨',
            'Body': '💆',
            'Nailcare': '💅'
        };

        let html = '';
        
        for (const [category, services] of Object.entries(grouped)) {
            html += `
                <div class="service-category" data-category="${category}">
                    <div class="category-header">
                        <span class="category-icon">${categoryIcons[category] || '💄'}</span>
                        <h2>${category} Services</h2>
                    </div>
                    <div class="services-grid">
                        ${services.map(service => `
                            <div class="service-item">
                                <div class="service-header">
                                    <h3>${service.name}</h3>
                                    <span class="service-price">${utils.formatPrice(service.price)}</span>
                                </div>
                                <p class="service-description">${service.description || 'Professional beauty service tailored to your needs.'}</p>
                                <div class="service-footer">
                                    <span class="service-duration">⏱ ${service.duration} min</span>
                                    <a href="booking.html?service=${service.id}" class="btn btn-outline btn-sm">Book Now</a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        servicesContainer.innerHTML = html;
    }

    /**
     * Setup category tab filters
     */
    function setupCategoryTabs() {
        categoryTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                categoryTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                currentCategory = tab.dataset.category;
                
                // Update URL without reload
                const url = new URL(window.location);
                if (currentCategory === 'all') {
                    url.searchParams.delete('category');
                } else {
                    url.searchParams.set('category', currentCategory);
                }
                window.history.pushState({}, '', url);
                
                renderServices();
            });
        });
    }
});
