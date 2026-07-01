(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initMobileMenu() {
    var toggle = document.querySelector('[data-menu-toggle]');
    var nav = document.querySelector('[data-mobile-nav]');
    var dock = document.querySelector('[data-mobile-dock]');
    var backdrop = document.querySelector('[data-menu-backdrop]');
    if (!toggle || !nav) return;

    var scrollY = 0;

    function setMenuOpen(isOpen) {
      nav.classList.toggle('is-open', isOpen);
      toggle.setAttribute('aria-expanded', String(isOpen));
      toggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');

      if (backdrop) {
        backdrop.classList.toggle('is-visible', isOpen);
        backdrop.hidden = !isOpen;
        backdrop.setAttribute('aria-hidden', String(!isOpen));
      }

      if (isOpen) {
        scrollY = window.scrollY;
        document.body.classList.add('is-menu-open');
        document.body.style.top = '-' + scrollY + 'px';
      } else {
        document.body.classList.remove('is-menu-open');
        document.body.style.top = '';
        window.scrollTo(0, scrollY);
      }
    }

    toggle.addEventListener('click', function () {
      setMenuOpen(!nav.classList.contains('is-open'));
    });

    if (backdrop) {
      backdrop.addEventListener('click', function () {
        setMenuOpen(false);
      });
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setMenuOpen(false);
      }
    });

    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        setMenuOpen(false);
      });
    });

    if (dock) {
      dock.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
          if (nav.classList.contains('is-open')) {
            setMenuOpen(false);
          }
        });
      });
    }
  }

  function animateCounter(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var suffix = el.getAttribute('data-suffix') || '';
    if (Number.isNaN(target)) return;

    if (prefersReducedMotion) {
      el.textContent = target + suffix;
      return;
    }

    var duration = 1400;
    var start = null;

    function tick(now) {
      if (!start) start = now;
      var progress = Math.min((now - start) / duration, 1);
      var eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      el.textContent = Math.round(eased * target) + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }

  function initReveal() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;

    function revealElement(el) {
      el.classList.add('is-visible');
      el.querySelectorAll('[data-count]').forEach(function (counter) {
        animateCounter(counter);
      });
    }

    if (!('IntersectionObserver' in window)) {
      items.forEach(revealElement);
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          revealElement(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -24px 0px' });

    items.forEach(function (el) { observer.observe(el); });

    window.setTimeout(function () {
      items.forEach(function (el) {
        if (!el.classList.contains('is-visible')) {
          revealElement(el);
        }
      });
    }, 1200);
  }

  function initHeaderScroll() {
    var header = document.getElementById('site-header');
    if (!header) return;

    function onScroll() {
      header.classList.toggle('is-scrolled', window.scrollY > 16);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  function initFilters(containerSelector, itemSelector) {
    var container = document.querySelector(containerSelector);
    if (!container) return;

    container.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-filter]');
      if (!btn) return;

      var filter = btn.getAttribute('data-filter');
      container.querySelectorAll('[data-filter]').forEach(function (b) {
        b.classList.toggle('filter-btn--active', b === btn);
      });

      document.querySelectorAll(itemSelector).forEach(function (item) {
        var category = item.getAttribute('data-category');
        var show = filter === 'all' || category === filter;
        item.style.display = show ? '' : 'none';
      });
    });
  }

  function initFaq() {
    var accordion = document.querySelector('[data-faq-accordion]');
    if (!accordion) return;

    accordion.addEventListener('click', function (e) {
      var trigger = e.target.closest('.faq-item__trigger');
      if (!trigger) return;

      var item = trigger.closest('.faq-item');
      var isOpen = item.classList.contains('is-open');

      accordion.querySelectorAll('.faq-item').forEach(function (el) {
        el.classList.remove('is-open');
        el.querySelector('.faq-item__panel').style.display = 'none';
        el.querySelector('.faq-item__trigger').setAttribute('aria-expanded', 'false');
        el.querySelector('.faq-item__icon').textContent = '+';
      });

      if (!isOpen) {
        item.classList.add('is-open');
        item.querySelector('.faq-item__panel').style.display = 'block';
        trigger.setAttribute('aria-expanded', 'true');
        item.querySelector('.faq-item__icon').textContent = '−';
      }
    });
  }

  function initServicePreselect() {
    var params = new URLSearchParams(window.location.search);
    var service = params.get('service');
    if (!service) return;

    document.querySelectorAll('[data-quote-form] select[name="service"]').forEach(function (select) {
      select.value = service;
    });
  }

  function initQuoteModal() {
    var modal = document.querySelector('[data-quote-modal]');
    if (!modal) return;

    var panel = modal.querySelector('.quote-modal__panel');
    var scrollY = 0;
    var lastTrigger = null;

    function getServiceSelect() {
      return modal.querySelector('[data-quote-form] select[name="service"]');
    }

    function setService(value) {
      var select = getServiceSelect();
      if (select && value) {
        select.value = value;
      }
    }

    function openModal(trigger) {
      lastTrigger = trigger || null;
      var service = trigger && trigger.getAttribute('data-service');
      setService(service || '');

      var nav = document.querySelector('[data-mobile-nav]');
      var menuToggle = document.querySelector('[data-menu-toggle]');
      var menuBackdrop = document.querySelector('[data-menu-backdrop]');
      if (nav && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        if (menuToggle) {
          menuToggle.setAttribute('aria-expanded', 'false');
          menuToggle.setAttribute('aria-label', 'Open menu');
        }
        if (menuBackdrop) {
          menuBackdrop.classList.remove('is-visible');
          menuBackdrop.hidden = true;
          menuBackdrop.setAttribute('aria-hidden', 'true');
        }
        document.body.classList.remove('is-menu-open');
        document.body.style.top = '';
        scrollY = window.scrollY;
      }

      modal.hidden = false;
      requestAnimationFrame(function () {
        modal.classList.add('is-open');
      });

      scrollY = window.scrollY;
      document.body.classList.add('is-quote-open');
      document.body.style.top = '-' + scrollY + 'px';

      var closeBtn = modal.querySelector('.quote-modal__close');
      if (closeBtn) closeBtn.focus();
    }

    function closeModal() {
      modal.classList.remove('is-open');
      document.body.classList.remove('is-quote-open');
      document.body.style.top = '';
      window.scrollTo(0, scrollY);

      window.setTimeout(function () {
        if (!modal.classList.contains('is-open')) {
          modal.hidden = true;
        }
      }, 360);

      if (lastTrigger) {
        lastTrigger.focus();
        lastTrigger = null;
      }
    }

    document.querySelectorAll('[data-quote-open]').forEach(function (trigger) {
      trigger.addEventListener('click', function (event) {
        event.preventDefault();
        openModal(trigger);
      });
    });

    modal.querySelectorAll('[data-quote-close]').forEach(function (el) {
      el.addEventListener('click', closeModal);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && modal.classList.contains('is-open')) {
        closeModal();
      }
    });

    modal.addEventListener('keydown', function (event) {
      if (event.key !== 'Tab' || !modal.classList.contains('is-open')) return;

      var focusable = modal.querySelectorAll(
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      );
      if (!focusable.length) return;

      var first = focusable[0];
      var last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }

  function bootDynamicUi() {
    try { initReveal(); } catch (e) { console.error(e); }
    try { initFilters('[data-blog-filters]', '#blog-content [data-category]'); } catch (e) { console.error(e); }
    if (window.initFormMasks) {
      try { window.initFormMasks(); } catch (e) { console.error(e); }
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    try { initMobileMenu(); } catch (e) { console.error(e); }
    try { initQuoteModal(); } catch (e) { console.error(e); }
    try { initHeaderScroll(); } catch (e) { console.error(e); }
    try { initFilters('[data-portfolio-filters]', '[data-portfolio-grid] .portfolio-card'); } catch (e) { console.error(e); }
    try { initFaq(); } catch (e) { console.error(e); }
    try { initServicePreselect(); } catch (e) { console.error(e); }
    bootDynamicUi();
  });

  document.body.addEventListener('htmx:afterSwap', function () {
    bootDynamicUi();
  });
})();
