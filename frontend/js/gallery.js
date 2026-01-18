/**
 * Jamie's Beauty Studio - Gallery Functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    const galleryGrid = document.getElementById('gallery-grid');
    const filterButtons = document.querySelectorAll('.gallery-filter-btn');
    const lightbox = document.getElementById('lightbox');
    
    let allImages = [];
    let currentFilter = 'all';

    // Initialize
    loadGallery();
    setupFilters();
    setupLightbox();

    /**
     * Load all gallery images
     */
    async function loadGallery() {
        if (!galleryGrid) return;

        // Placeholder images for different categories
        const placeholderData = [
            { id: 1, category: 'Hair', alt_text: 'Elegant updo hairstyle', url: 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=600&h=600&fit=crop' },
            { id: 2, category: 'Hair', alt_text: 'Natural balayage highlights', url: 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&h=600&fit=crop' },
            { id: 3, category: 'Hair', alt_text: 'Bridal hair styling', url: 'https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?w=600&h=600&fit=crop' },
            { id: 4, category: 'Facial', alt_text: 'Relaxing facial treatment', url: 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=600&h=600&fit=crop' },
            { id: 5, category: 'Facial', alt_text: 'Glowing skin result', url: 'https://images.unsplash.com/photo-1512290923902-8a9f81dc236c?w=600&h=600&fit=crop' },
            { id: 6, category: 'Nailcare', alt_text: 'Artistic nail design', url: 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=600&h=600&fit=crop' },
            { id: 7, category: 'Nailcare', alt_text: 'French tip manicure', url: 'https://images.unsplash.com/photo-1519014816548-bf5fe059798b?w=600&h=600&fit=crop' },
            { id: 8, category: 'Body', alt_text: 'Spa massage treatment', url: 'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=600&h=600&fit=crop' },
            { id: 9, category: 'Studio', alt_text: 'Beauty studio interior', url: 'https://images.unsplash.com/photo-1633681926022-84c23e8cb2d6?w=600&h=600&fit=crop' },
            { id: 10, category: 'Hair', alt_text: 'Color transformation', url: 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=600&h=600&fit=crop' },
            { id: 11, category: 'Facial', alt_text: 'Skincare treatment', url: 'https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=600&h=600&fit=crop' },
            { id: 12, category: 'Studio', alt_text: 'Product collection', url: 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&h=600&fit=crop' }
        ];

        try {
            // Try to load from API first
            const apiImages = await api.get('/api/gallery');
            
            // Merge API data with placeholder URLs
            allImages = apiImages.map((img, index) => ({
                ...img,
                url: placeholderData[index]?.url || placeholderData[0].url
            }));
        } catch (error) {
            console.error('Failed to load gallery from API, using placeholders:', error);
            allImages = placeholderData;
        }

        renderGallery(allImages);
    }

    /**
     * Render gallery images
     */
    function renderGallery(images) {
        if (!galleryGrid) return;

        galleryGrid.innerHTML = images.map((img, index) => `
            <div class="gallery-item ${index === 0 ? 'gallery-item-large' : ''}" 
                 data-category="${img.category}"
                 data-index="${index}">
                <img src="${img.url}" alt="${img.alt_text}" loading="lazy">
                <div class="gallery-overlay">
                    <span class="gallery-category">${img.category}</span>
                    <span class="gallery-zoom">🔍</span>
                </div>
            </div>
        `).join('');

        // Add click handlers for lightbox
        document.querySelectorAll('.gallery-item').forEach(item => {
            item.addEventListener('click', () => {
                const index = parseInt(item.dataset.index);
                openLightbox(index);
            });
        });
    }

    /**
     * Setup filter buttons
     */
    function setupFilters() {
        if (!filterButtons.length) return;

        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active state
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Filter images
                currentFilter = btn.dataset.filter;
                
                if (currentFilter === 'all') {
                    renderGallery(allImages);
                } else {
                    const filtered = allImages.filter(img => img.category === currentFilter);
                    renderGallery(filtered);
                }
            });
        });
    }

    /**
     * Setup lightbox functionality
     */
    function setupLightbox() {
        if (!lightbox) return;

        // Create lightbox HTML if it doesn't exist
        if (!lightbox.innerHTML.trim()) {
            lightbox.innerHTML = `
                <div class="lightbox-content">
                    <button class="lightbox-close" aria-label="Close">&times;</button>
                    <button class="lightbox-prev" aria-label="Previous">&larr;</button>
                    <button class="lightbox-next" aria-label="Next">&rarr;</button>
                    <img class="lightbox-image" src="" alt="">
                    <div class="lightbox-caption"></div>
                </div>
            `;
        }

        // Close button
        lightbox.querySelector('.lightbox-close')?.addEventListener('click', closeLightbox);
        
        // Navigation
        lightbox.querySelector('.lightbox-prev')?.addEventListener('click', () => navigateLightbox(-1));
        lightbox.querySelector('.lightbox-next')?.addEventListener('click', () => navigateLightbox(1));

        // Close on background click
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) closeLightbox();
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (!lightbox.classList.contains('active')) return;
            
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowLeft') navigateLightbox(-1);
            if (e.key === 'ArrowRight') navigateLightbox(1);
        });
    }

    let currentLightboxIndex = 0;

    /**
     * Open lightbox
     */
    function openLightbox(index) {
        if (!lightbox) return;

        currentLightboxIndex = index;
        const filteredImages = currentFilter === 'all' 
            ? allImages 
            : allImages.filter(img => img.category === currentFilter);
        
        const image = filteredImages[index];
        if (!image) return;

        const lightboxImg = lightbox.querySelector('.lightbox-image');
        const lightboxCaption = lightbox.querySelector('.lightbox-caption');

        lightboxImg.src = image.url;
        lightboxImg.alt = image.alt_text;
        lightboxCaption.textContent = image.alt_text;

        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    /**
     * Close lightbox
     */
    function closeLightbox() {
        if (!lightbox) return;

        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }

    /**
     * Navigate lightbox
     */
    function navigateLightbox(direction) {
        const filteredImages = currentFilter === 'all' 
            ? allImages 
            : allImages.filter(img => img.category === currentFilter);

        currentLightboxIndex += direction;
        
        if (currentLightboxIndex < 0) {
            currentLightboxIndex = filteredImages.length - 1;
        } else if (currentLightboxIndex >= filteredImages.length) {
            currentLightboxIndex = 0;
        }

        const image = filteredImages[currentLightboxIndex];
        const lightboxImg = lightbox.querySelector('.lightbox-image');
        const lightboxCaption = lightbox.querySelector('.lightbox-caption');

        lightboxImg.src = image.url;
        lightboxImg.alt = image.alt_text;
        lightboxCaption.textContent = image.alt_text;
    }
});
