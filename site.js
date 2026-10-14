(function () {
  document.documentElement.classList.remove('no-js');

  // Scroll-Einblendung (aus bei prefers-reduced-motion)
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (e) { e.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (e) { io.observe(e); });
  }

  // Umschalter Smartphone | Desktop: Buttons und Panels über data-group und data-target
  document.querySelectorAll('.seg button[data-group]').forEach(function (b) {
    b.addEventListener('click', function () {
      var g = b.getAttribute('data-group');
      document.querySelectorAll('[data-group="' + g + '"]').forEach(function (el) {
        if (el.tagName === 'BUTTON') el.setAttribute('aria-pressed', String(el === b));
        else el.hidden = el.id !== b.getAttribute('data-target');
      });
    });
  });

  // Demo-Video: Button in index.html ist ausgeblendet, bis video/demo.mp4 existiert (hidden entfernen)
  var openBtn = document.getElementById('demo-open'), dlg = document.getElementById('demo-dialog');
  if (openBtn && dlg) {
    var vid = document.getElementById('demo-video');
    openBtn.addEventListener('click', function () {
      if (!vid.getAttribute('src')) { vid.src = 'video/demo.mp4'; vid.poster = 'video/demo-poster.webp'; }
      dlg.showModal();
    });
    dlg.addEventListener('close', function () { vid.pause(); });
  }
})();
