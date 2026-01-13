document.addEventListener('DOMContentLoaded', function() {
  const hamburger = document.querySelector('.hamburger-btn');
  const mobileMenu = document.querySelector('.mobile-menu');
  const header = document.querySelector('.site-header');

  if (hamburger && mobileMenu) {
    const closeMenu = function() {
      mobileMenu.classList.remove('active');
      hamburger.setAttribute('aria-expanded', 'false');
    };

    hamburger.addEventListener('click', function() {
      const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', String(!isExpanded));
      mobileMenu.classList.toggle('active');
    });

    mobileMenu.querySelectorAll('a').forEach(function(link) {
      link.addEventListener('click', closeMenu);
    });

    window.addEventListener('resize', function() {
      if (window.innerWidth > 600) {
        closeMenu();
      }
    });
  }

  if (header) {
    const toggleHeader = function() {
      header.classList.toggle('is-scrolled', window.scrollY > 10);
    };
    toggleHeader();
    window.addEventListener('scroll', toggleHeader, { passive: true });
  }
});
