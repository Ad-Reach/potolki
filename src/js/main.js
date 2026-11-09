(function () {
  var C = window.SITE || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* header: glass on top, white after scroll */
  var hdr = $('.hdr');
  function onScroll() { if (hdr) hdr.classList.toggle('solid', window.scrollY > 40 || document.body.classList.contains('light-top')); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* burger */
  var burger = $('.burger'), mob = $('.mob');
  if (burger) burger.addEventListener('click', function () {
    var o = mob.classList.toggle('open'); burger.setAttribute('aria-expanded', o); if (o) hdr.classList.add('solid'); else onScroll();
  });
  $$('.dd>button').forEach(function (b) {
    b.addEventListener('click', function () { var o = b.parentNode.classList.toggle('open'); b.setAttribute('aria-expanded', o); });
  });
  document.addEventListener('click', function (e) { $$('.dd.open').forEach(function (d) { if (!d.contains(e.target)) d.classList.remove('open'); }); });

  /* hero slider: autoplay + arrows + swipe */
  var hero = $('.hero');
  if (hero) {
    var imgs = $$('.hero-slides img', hero), dots = $$('.hero-dots i', hero), cnt = $('.hero-ctrl span', hero);
    var i = 0, t, INT = C.heroInterval || 2000;
    hero.style.setProperty('--int', INT + 'ms');
    var pad = function (x) { return (x < 10 ? '0' : '') + x; };
    function show(n) {
      i = (n + imgs.length) % imgs.length;
      imgs.forEach(function (im, k) { im.classList.toggle('on', k === i); if (k === i && im.dataset.src) { im.src = im.dataset.src; im.removeAttribute('data-src'); } });
      var nx = imgs[(i + 1) % imgs.length]; if (nx.dataset.src) { nx.src = nx.dataset.src; nx.removeAttribute('data-src'); }
      dots.forEach(function (d, k) { d.classList.remove('on'); if (k === i) { void d.offsetWidth; d.classList.add('on'); } });
      if (cnt) cnt.textContent = pad(i + 1) + ' / ' + pad(imgs.length);
      clearTimeout(t); t = setTimeout(function () { show(i + 1); }, INT);
    }
    $('.hero-ctrl .prev', hero).addEventListener('click', function () { show(i - 1); });
    $('.hero-ctrl .next', hero).addEventListener('click', function () { show(i + 1); });
    var x0 = null;
    hero.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1)); x0 = null; });
    show(0);
  }

  /* calculator */
  $$('.calc').forEach(function (calc) {
    var P = C.prices; if (!P) return;
    var st = { area: 18, canvas: calc.dataset.canvas || 'mat', profile: 'std', lamps: 4, corners: 4 };
    var area = $('[name=area]', calc), areaOut = $('.area-out', calc), sum = $('.calc-sum b', calc), note = $('.calc-note', calc);
    function fmt(n) { return Math.round(n).toLocaleString('ru-RU') + ' ₽'; }
    function upd() {
      var per = Math.sqrt(st.area) * 4.2;
      var c = P.canvas[st.canvas], pr = P.profile[st.profile];
      var total = st.area * c.m2 + per * pr.m + st.lamps * P.lamp + Math.max(0, st.corners - 4) * P.corner;
      total = Math.max(total, P.min || 0);
      sum.textContent = 'от ' + fmt(total);
      areaOut.textContent = st.area + ' м²';
      note.textContent = 'Расчёт: ' + st.area + ' м², полотно ' + c.name.toLowerCase() + ', ' + pr.name.toLowerCase() + ', светильников: ' + st.lamps + '. Точная смета — после бесплатного замера, и она уже не изменится.';
      $$('.chip', calc).forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.v === st.canvas); });
    }
    area.addEventListener('input', function () { st.area = +area.value; upd(); });
    $$('.chip', calc).forEach(function (b) { b.addEventListener('click', function () { st.canvas = b.dataset.v; upd(); }); });
    $('[name=profile]', calc).addEventListener('change', function (e) { st.profile = e.target.value; upd(); });
    $$('.num', calc).forEach(function (n) {
      var k = n.dataset.k, o = $('output', n);
      $$('button', n).forEach(function (b) { b.addEventListener('click', function () { st[k] = Math.max(0, st[k] + (+b.dataset.d)); o.textContent = st[k]; upd(); }); });
    });
    upd();
  });

  /* reveal on scroll */
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: .15 }) : null;
  $$('.rv,.geo').forEach(function (el) { if (io) io.observe(el); else el.classList.add('in'); });

  /* steps progress bar fills while scrolling */
  var steps = $('.steps');
  if (steps) {
    var bar = $('.steps-bar i', steps), items = $$('li', steps);
    var stepsTick = function () {
      var r = steps.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
      bar.style.width = (p * 100) + '%'; bar.style.setProperty('--h', (p * 100) + '%');
      items.forEach(function (li, k) { li.classList.toggle('on', p >= k / (items.length - 1) - 0.001); });
    };
    window.addEventListener('scroll', stepsTick, { passive: true }); window.addEventListener('resize', stepsTick); stepsTick();
  }

  /* tabs + gallery (works page) */
  $$('[role=tablist]').forEach(function (tl) {
    var tabs = $$('[role=tab]', tl);
    tabs.forEach(function (tb) {
      tb.addEventListener('click', function () {
        tabs.forEach(function (x) { x.setAttribute('aria-selected', x === tb); var p = document.getElementById(x.getAttribute('aria-controls')); if (p) p.hidden = x !== tb; });
      });
    });
  });
  $$('.gal').forEach(function (g) {
    var main = $('.gal-main img', g), th = $$('.thumbs button', g), k = 0;
    function go(n) { k = (n + th.length) % th.length; main.src = th[k].dataset.full; th.forEach(function (b, j) { b.setAttribute('aria-current', j === k); }); }
    th.forEach(function (b, j) { b.addEventListener('click', function () { go(j); }); });
    $('.prev', g).addEventListener('click', function () { go(k - 1); });
    $('.next', g).addEventListener('click', function () { go(k + 1); });
  });

  /* lightbox */
  var lb = $('.lb');
  if (lb) {
    $$('.gallery a').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); $('img', lb).src = a.href; lb.classList.add('open'); }); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('x')) lb.classList.remove('open'); });
  }

  /* callback modal */
  var modal = $('.modal');
  $$('[data-cb]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); modal.classList.add('open'); var f = $('input[type=tel]', modal); if (f) f.focus(); }); });
  if (modal) modal.addEventListener('click', function (e) { if (e.target === modal || e.target.classList.contains('x')) modal.classList.remove('open'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { if (modal) modal.classList.remove('open'); if (lb) lb.classList.remove('open'); } });

  /* forms: open WhatsApp with the request text (no backend yet) */
  $$('form.form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.checkValidity()) { f.reportValidity(); return; }
      var name = (f.elements.name && f.elements.name.value) || '', tel = f.elements.tel.value;
      var txt = 'Здравствуйте! Заявка с сайта centro-plus.ru' + (f.dataset.topic ? ' (' + f.dataset.topic + ')' : '') + '.\nИмя: ' + name + '\nТелефон: ' + tel;
      window.open('https://wa.me/' + C.wa + '?text=' + encodeURIComponent(txt), '_blank');
      f.classList.add('sent');
    });
  });
})();
