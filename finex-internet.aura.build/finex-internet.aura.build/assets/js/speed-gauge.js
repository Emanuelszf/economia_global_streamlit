/* Hero bandwidth gauge animation.
   Drives the SVG #gauge-needle / #gauge-progress using a smoothed sine
   wave (with light random noise) to simulate a live speed test. The
   stop/start button (id="stop-test-btn") toggles the loop and swaps
   icon + label. */
(function () {
  const needle = document.getElementById('gauge-needle');
  const progress = document.getElementById('gauge-progress');
  const valEl = document.getElementById('speed-value');
  const decEl = document.getElementById('speed-decimal');
  const btn = document.getElementById('stop-test-btn');
  const btnText = document.getElementById('stop-btn-text');
  const btnIcon = document.getElementById('stop-btn-icon');

  // Gauge configuration
  const MAX_SPEED = 1000;
  const MAX_STROKE = 612;   // 270deg arc length for r=130
  const START_ANGLE = 135;
  const RANGE_ANGLE = 270;

  let isTesting = true;
  let animationId;
  let currentSmoothedSpeed = null;

  function updateGauge(speed) {
    const clampedSpeed = Math.min(Math.max(speed, 0), MAX_SPEED);
    const normalized = clampedSpeed / MAX_SPEED;

    const rotation = START_ANGLE + (normalized * RANGE_ANGLE);
    if (needle) needle.setAttribute('transform', `rotate(${rotation} 150 150)`);

    const dash = normalized * MAX_STROKE;
    if (progress) progress.style.strokeDasharray = `${dash} 1000`;

    if (valEl) valEl.textContent = Math.floor(clampedSpeed);
    if (decEl) decEl.textContent = Math.floor((clampedSpeed % 1) * 10);
  }

  function loop(timestamp) {
    if (!isTesting) return;

    const time = timestamp / 2000;
    const wave = (Math.sin(time) + 1) / 2;
    const noise = (Math.random() * 10 - 5);

    let targetSpeed = (wave * MAX_SPEED) + noise;
    if (currentSmoothedSpeed === null) currentSmoothedSpeed = targetSpeed;
    currentSmoothedSpeed += (targetSpeed - currentSmoothedSpeed) * 0.05;

    updateGauge(Math.max(0, Math.min(MAX_SPEED, currentSmoothedSpeed)));
    animationId = requestAnimationFrame(loop);
  }

  if (btn) {
    btn.addEventListener('click', () => {
      isTesting = !isTesting;

      if (isTesting) {
        if (btnText) btnText.textContent = 'Parar Teste';
        if (btnIcon) btnIcon.innerHTML =
          '<rect x="6" y="4" width="4" height="16" rx="1" ry="1"></rect>' +
          '<rect x="14" y="4" width="4" height="16" rx="1" ry="1"></rect>';
        loop(performance.now());
      } else {
        if (btnText) btnText.textContent = 'Iniciar Novo Teste';
        if (btnIcon) btnIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"></polygon>';
        if (animationId) cancelAnimationFrame(animationId);
      }
    });
  }

  loop(performance.now());
})();
