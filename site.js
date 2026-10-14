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

  // Plattform-Umschalter im Hero
  var ios = document.getElementById('hero-ios'), web = document.getElementById('hero-web');
  document.querySelectorAll('.plat-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var isIos = b.getAttribute('data-platform') === 'ios';
      if (ios) ios.hidden = !isIos;
      if (web) web.hidden = isIos;
      document.querySelectorAll('.plat-btn').forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
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
