/* Staggered word reveal driven by GSAP + ScrollTrigger.
   Walks every text node inside `.staggered-reveal` headings, wraps each
   word in <span class="reveal-word-mask"><span class="reveal-word-inner">,
   then animates each inner span up from translateY(110%) when its parent
   enters the viewport. */
const initReveal = () => {
  gsap.registerPlugin(ScrollTrigger);
  const t = document.querySelectorAll(".staggered-reveal");
  t.forEach((e) => {
    const r = document.createTreeWalker(e, NodeFilter.SHOW_TEXT, null, !1);
    const n = [];
    let l;
    for (; (l = r.nextNode()); ) {
      if (l.textContent.trim().length > 0) n.push(l);
    }
    n.forEach((r) => {
      const words = r.textContent.split(/\s+/).filter((e) => e.trim().length > 0);
      const frag = document.createDocumentFragment();
      words.forEach((w, idx) => {
        const span = document.createElement("span");
        span.className = "reveal-word-mask";
        span.innerHTML = `<span class="reveal-word-inner">${w}</span>`;
        frag.appendChild(span);
        if (idx < words.length - 1) frag.appendChild(document.createTextNode(" "));
      });
      r.parentNode.replaceChild(frag, r);
    });
    gsap.fromTo(
      e.querySelectorAll(".reveal-word-inner"),
      { y: "110%" },
      {
        y: "0%",
        duration: 1,
        ease: "power4.out",
        stagger: 0.03,
        scrollTrigger: { trigger: e, start: "top 85%", toggleActions: "play none none reverse" }
      }
    );
  });
};

const check = () => {
  window.gsap && window.ScrollTrigger ? initReveal() : setTimeout(check, 50);
};
check();
