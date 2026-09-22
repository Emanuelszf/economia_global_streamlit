// Typing animation for the IDE code panel and counter animation for stats
document.addEventListener('DOMContentLoaded', () => {
  // Typing Animation
  const textToType = "setStatus('active');";
  const typingElement = document.getElementById('typing-text');
  let index = 0;

  function typeWriter() {
    if (!typingElement) return;
    if (index < textToType.length) {
      typingElement.innerHTML += textToType.charAt(index);
      index++;
      setTimeout(typeWriter, 100);
    } else {
      setTimeout(() => {
        typingElement.innerHTML = "";
        index = 0;
        typeWriter();
      }, 3000);
    }
  }
  setTimeout(typeWriter, 1000);

  // Counter Animation
  const counters = document.querySelectorAll('.counter');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const counter = entry.target;
        const target = parseFloat(counter.getAttribute('data-target'));
        const duration = 2000;
        const start = performance.now();

        function step(timestamp) {
          const progress = Math.min((timestamp - start) / duration, 1);
          const ease = 1 - Math.pow(1 - progress, 4);
          counter.innerText = (target * ease).toFixed(2) + "%";
          if (progress < 1) {
            window.requestAnimationFrame(step);
          } else {
            counter.innerText = target + "%";
          }
        }
        window.requestAnimationFrame(step);
        observer.unobserve(counter);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => observer.observe(c));
});
