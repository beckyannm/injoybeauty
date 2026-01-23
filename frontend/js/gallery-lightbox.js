/**
 * Gallery Lightbox for Mobile Devices
 * Provides full-screen image viewing with swipe navigation
 */

(function() {
    'use strict';

    // Only run on mobile devices
    if (window.innerWidth >= 768) {
        return;
    }

    const lightbox = document.getElementById('gallery-lightbox');
    const lightboxImage = lightbox?.querySelector('.lightbox-image');
    const lightboxClose = lightbox?.querySelector('.lightbox-close');
    const lightboxPrev = lightbox?.querySelector('.lightbox-prev');
    const lightboxNext = lightbox?.querySelector('.lightbox-next');

    if (!lightbox || !lightboxImage) return;

    let currentImages = [];
    let currentIndex = 0;
    let touchStartX = 0;
    let touchEndX = 0;
    let isTransitioning = false;

    /**
     * Initialize gallery lightbox
     */
    function init() {
        // Find all gallery grids
        const galleryGrids = document.querySelectorAll('.gallery-grid');

        galleryGrids.forEach((grid) => {
            const galleryItems = grid.querySelectorAll('.gallery-item');
            
            galleryItems.forEach((item, itemIndex) => {
                const img = item.querySelector('img');
                if (!img) return;

                // Make items clickable
                item.style.cursor = 'pointer';
                
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    openLightbox(grid, itemIndex);
                });
            });
        });

        // Setup lightbox controls (only once)
        if (lightboxClose && !lightboxClose.dataset.initialized) {
            lightboxClose.addEventListener('click', closeLightbox);
            lightboxClose.dataset.initialized = 'true';
        }

        if (lightboxPrev && !lightboxPrev.dataset.initialized) {
            lightboxPrev.addEventListener('click', () => navigate(-1));
            lightboxPrev.dataset.initialized = 'true';
        }

        if (lightboxNext && !lightboxNext.dataset.initialized) {
            lightboxNext.addEventListener('click', () => navigate(1));
            lightboxNext.dataset.initialized = 'true';
        }

        // Close on background click (only once)
        if (!lightbox.dataset.initialized) {
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox) {
                    closeLightbox();
                }
            });
            lightbox.dataset.initialized = 'true';
        }

        // Keyboard navigation (only once)
        if (!document.galleryLightboxKeydown) {
            document.addEventListener('keydown', handleKeydown);
            document.galleryLightboxKeydown = true;
        }

        // Touch swipe support (only once)
        if (!lightboxImage.dataset.swipeInitialized) {
            lightboxImage.addEventListener('touchstart', handleTouchStart, { passive: true });
            lightboxImage.addEventListener('touchend', handleTouchEnd, { passive: true });
            lightboxImage.dataset.swipeInitialized = 'true';
        }
    }

    /**
     * Open lightbox with images from a specific gallery grid
     */
    function openLightbox(grid, startIndex) {
        const galleryItems = grid.querySelectorAll('.gallery-item');
        currentImages = Array.from(galleryItems).map(item => {
            const img = item.querySelector('img');
            const overlay = item.querySelector('.gallery-overlay span');
            return {
                src: img?.src || '',
                alt: img?.alt || '',
                caption: overlay?.textContent || ''
            };
        }).filter(img => img.src);

        if (currentImages.length === 0) return;

        currentIndex = Math.max(0, Math.min(startIndex, currentImages.length - 1));
        updateImage();
        
        // Show lightbox with smooth transition
        requestAnimationFrame(() => {
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    /**
     * Close lightbox
     */
    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
        currentImages = [];
        currentIndex = 0;
    }

    /**
     * Navigate to previous/next image
     */
    function navigate(direction) {
        if (isTransitioning || currentImages.length === 0) return;

        currentIndex += direction;
        
        if (currentIndex < 0) {
            currentIndex = currentImages.length - 1;
        } else if (currentIndex >= currentImages.length) {
            currentIndex = 0;
        }

        updateImage();
    }

    /**
     * Update lightbox image
     */
    function updateImage() {
        if (currentImages.length === 0 || !currentImages[currentIndex]) return;

        isTransitioning = true;
        
        // Fade out
        lightboxImage.style.transition = 'opacity 0.3s ease';
        lightboxImage.style.opacity = '0';
        
        setTimeout(() => {
            const image = currentImages[currentIndex];
            lightboxImage.src = image.src;
            lightboxImage.alt = image.alt;
            
            // Fade in
            requestAnimationFrame(() => {
                lightboxImage.style.opacity = '1';
                setTimeout(() => {
                    isTransitioning = false;
                }, 300);
            });
        }, 150);
    }

    /**
     * Handle keyboard navigation
     */
    function handleKeydown(e) {
        if (!lightbox.classList.contains('active')) return;

        if (e.key === 'Escape') {
            closeLightbox();
        } else if (e.key === 'ArrowLeft') {
            navigate(-1);
        } else if (e.key === 'ArrowRight') {
            navigate(1);
        }
    }

    /**
     * Handle touch start for swipe
     */
    function handleTouchStart(e) {
        touchStartX = e.changedTouches[0].screenX;
    }

    /**
     * Handle touch end for swipe
     */
    function handleTouchEnd(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }

    /**
     * Process swipe gesture
     */
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe left - next image
                navigate(1);
            } else {
                // Swipe right - previous image
                navigate(-1);
            }
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Re-initialize on resize if switching to mobile
    let isMobile = window.innerWidth < 768;
    window.addEventListener('resize', () => {
        const nowMobile = window.innerWidth < 768;
        if (!isMobile && nowMobile) {
            // Switched to mobile, re-initialize
            init();
        }
        isMobile = nowMobile;
    });
})();
