/* Testimonials section: scroll-driven active state.
   Uses an IntersectionObserver tuned to the middle of the viewport
   (rootMargin -45% top/bottom) to highlight whichever .testimonial-item
   is centered, syncing the matching .avatar-indicator. Avatars are also
   clickable to scroll to the matching quote. */
(function () {
  const options = {
    root: null,
    rootMargin: '-45% 0px -45% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const index = entry.target.getAttribute('data-index');
        updateActiveState(index);
      }
    });
  }, options);

  const items = document.querySelectorAll('.testimonial-item');
  items.forEach((item) => observer.observe(item));

  const avatars = document.querySelectorAll('.avatar-indicator');
  avatars.forEach((avatar) => {
    avatar.addEventListener('click', () => {
      const targetIndex = avatar.getAttribute('data-target');
      const targetItem = document.querySelector(`.testimonial-item[data-index="${targetIndex}"]`);
      if (targetItem) {
        targetItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
        updateActiveState(targetIndex);
      }
    });
  });

  function updateActiveState(index) {
    items.forEach((item) => {
      item.classList.toggle('active', item.getAttribute('data-index') === index);
    });
    avatars.forEach((avatar) => {
      avatar.classList.toggle('active', avatar.getAttribute('data-target') === index);
    });
  }

  setTimeout(() => updateActiveState('0'), 100);
})();
