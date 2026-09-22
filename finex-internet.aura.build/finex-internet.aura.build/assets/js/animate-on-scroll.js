/* In-view animation kicker.
   Watches elements matching `.animate-on-scroll` (default selector) and
   adds an `.animate` class once they enter the viewport so any keyframe
   animation set via Tailwind utilities (e.g. [animation:animationIn_...])
   runs on scroll instead of on page load. */
(function () {
  // Inject CSS for paused/running states (kept here so the behavior is self-contained).
  const style = document.createElement("style");
  style.textContent = `
    .animate-on-scroll { animation-play-state: paused !important; }
    .animate-on-scroll.animate { animation-play-state: running !important; }
  `;
  document.head.appendChild(style);

  const once = true;
  if (!window.__inViewIO) {
    window.__inViewIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("animate");
            if (once) window.__inViewIO.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2, rootMargin: "0px 0px -10% 0px" }
    );
  }

  window.initInViewAnimations = function (selector = ".animate-on-scroll") {
    document.querySelectorAll(selector).forEach((el) => {
      window.__inViewIO.observe(el);
    });
  };

  document.addEventListener("DOMContentLoaded", () => initInViewAnimations());
})();
