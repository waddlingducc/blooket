// Load the hero animations first, without waiting for scroll position
const riveAnims = [
  {
    src: 'https://ac.blooket.com/www/assets/animations/owlV2.riv',
    canvasId: 'owl',
  },
  {
    src: 'https://ac.blooket.com/www/assets/animations/chicks.riv',
    canvasId: 'chicks',
  },
];

const visibilityObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    const r = entry.target.__riveInstance;
    if (!r) return;
    if (entry.isIntersecting) {
      try { r.play(); } catch (_) {}
    } else {
      try { r.pause(); } catch (_) {}
    }
  });
}, { rootMargin: '100px 0px 100px 0px' });

document.addEventListener('visibilitychange', () => {
  document.querySelectorAll('canvas.sectionCanvas').forEach((el) => {
    const r = el.__riveInstance;
    if (!r) return;
    try { document.hidden ? r.pause() : r.play(); } catch (_) {}
  });
});

riveAnims.forEach((data) => {
  const el = document.getElementById(data.canvasId);
  if (!el) return;
  const r = new rive.Rive({
    src: data.src,
    canvas: el,
    autoplay: false,
    onLoad: () => {
      r.resizeDrawingSurfaceToCanvas();
      el.__riveInstance = r;
      setTimeout(() => {
        r.play();
        el.classList.add('loaded');
        visibilityObserver.observe(el);
      }, 10);
    },
  });
});
