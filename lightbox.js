(function () {
  var style = document.createElement('style');
  style.textContent =
    '.lb-trigger{cursor:zoom-in}' +
    '.lb-overlay{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;' +
    'background:rgba(3,7,18,.92);padding:2rem;opacity:0;pointer-events:none;transition:opacity .15s ease}' +
    '.lb-overlay.lb-open{opacity:1;pointer-events:auto}' +
    '.lb-overlay img{max-width:min(90vw,1100px);max-height:88vh;width:auto;height:auto;border-radius:.75rem;' +
    'box-shadow:0 25px 50px -12px rgba(0,0,0,.6)}' +
    '.lb-close{position:absolute;top:1.25rem;right:1.5rem;color:#fff;opacity:.7;font-size:2rem;line-height:1;' +
    'cursor:pointer;background:none;border:0;padding:.5rem}' +
    '.lb-close:hover{opacity:1}';
  document.head.appendChild(style);

  var overlay = document.createElement('div');
  overlay.className = 'lb-overlay';
  overlay.innerHTML = '<button class="lb-close" aria-label="Schließen">&times;</button><img alt="" />';
  document.body.appendChild(overlay);
  var overlayImg = overlay.querySelector('img');

  function open(src, alt) {
    overlayImg.src = src;
    overlayImg.alt = alt || '';
    overlay.classList.add('lb-open');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    overlay.classList.remove('lb-open');
    document.body.style.overflow = '';
  }

  overlay.addEventListener('click', function (e) {
    if (e.target === overlay || e.target.classList.contains('lb-close')) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
  });

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('img.lb-trigger').forEach(function (img) {
      img.addEventListener('click', function () {
        open(img.currentSrc || img.src, img.alt);
      });
    });
  });
})();
