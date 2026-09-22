/* Page interactions:
   - Initialize Lucide icons.
   - aura-reveal IntersectionObserver: adds `is-visible` so the entrance
     animation runs once an element scrolls into view. Cascading delay
     is auto-applied per sibling order (100ms steps).
   - flashlight-card: tracks the mouse and writes --mouse-x / --mouse-y
     CSS variables consumed by the radial spotlight pseudo-element. */
lucide.createIcons();

document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });

  document.querySelectorAll('.aura-reveal').forEach((el) => {
    const parent = el.parentElement;
    if (parent) {
      const siblings = Array.from(parent.children).filter(c => c.classList.contains('aura-reveal'));
      const index = siblings.indexOf(el);
      if (index > 0) el.style.animationDelay = `${index * 100}ms`;
    }
    observer.observe(el);
  });

  document.querySelectorAll('.flashlight-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
      card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
    });
  });
});
