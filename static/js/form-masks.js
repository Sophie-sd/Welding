(function () {
  'use strict';

  function formatName(value) {
    return value
      .replace(/[^a-zA-Z\s'-]/g, '')
      .replace(/\s{2,}/g, ' ')
      .replace(/^\s+/, '');
  }

  function formatUKPhone(value) {
    var digits = value.replace(/\D/g, '');

    if (digits.indexOf('44') === 0) {
      digits = digits.slice(2);
    }
    if (digits.indexOf('0') === 0) {
      digits = digits.slice(1);
    }

    digits = digits.slice(0, 10);

    if (!digits.length) {
      return '';
    }

    var parts = ['+44'];
    if (digits.length <= 4) {
      parts.push(digits);
    } else if (digits.length <= 7) {
      parts.push(digits.slice(0, 4), digits.slice(4));
    } else {
      parts.push(digits.slice(0, 4), digits.slice(4, 7), digits.slice(7));
    }

    return parts.join(' ');
  }

  function isValidEmail(value) {
    if (!value) {
      return true;
    }
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value);
  }

  function setFieldState(input, isValid) {
    input.classList.toggle('form-input--invalid', !isValid);
    input.setAttribute('aria-invalid', isValid ? 'false' : 'true');
  }

  function bindFormMasks(form) {
    var nameInput = form.querySelector('[data-mask="name"]');
    var phoneInput = form.querySelector('[data-mask="phone"]');
    var emailInput = form.querySelector('[data-mask="email"]');

    if (nameInput) {
      nameInput.addEventListener('input', function () {
        var cursor = nameInput.selectionStart;
        nameInput.value = formatName(nameInput.value);
        nameInput.setSelectionRange(cursor, cursor);
        setFieldState(nameInput, nameInput.value.trim().length >= 2);
      });
    }

    if (phoneInput) {
      phoneInput.addEventListener('input', function () {
        phoneInput.value = formatUKPhone(phoneInput.value);
        var digits = phoneInput.value.replace(/\D/g, '');
        setFieldState(phoneInput, digits.length >= 12);
      });

      phoneInput.addEventListener('focus', function () {
        if (!phoneInput.value) {
          phoneInput.value = '+44 ';
        }
      });

      phoneInput.addEventListener('blur', function () {
        if (phoneInput.value.trim() === '+44') {
          phoneInput.value = '';
        }
      });
    }

    if (emailInput) {
      emailInput.addEventListener('input', function () {
        emailInput.value = emailInput.value.replace(/\s/g, '').toLowerCase();
        setFieldState(emailInput, isValidEmail(emailInput.value));
      });

      emailInput.addEventListener('blur', function () {
        setFieldState(emailInput, isValidEmail(emailInput.value));
      });
    }

    form.addEventListener('submit', function (event) {
      var valid = true;

      if (nameInput && nameInput.value.trim().length < 2) {
        setFieldState(nameInput, false);
        valid = false;
      }

      if (phoneInput && phoneInput.value.replace(/\D/g, '').length < 12) {
        setFieldState(phoneInput, false);
        valid = false;
      }

      if (emailInput && emailInput.value && !isValidEmail(emailInput.value)) {
        setFieldState(emailInput, false);
        valid = false;
      }

      if (!valid) {
        event.preventDefault();
      }
    });
  }

  function initFormMasks() {
    document.querySelectorAll('[data-quote-form]').forEach(function (form) {
      if (form.dataset.masksBound === '1') {
        return;
      }
      form.dataset.masksBound = '1';
      bindFormMasks(form);
    });
  }

  window.initFormMasks = initFormMasks;

  document.addEventListener('DOMContentLoaded', initFormMasks);
  document.body.addEventListener('htmx:afterSwap', initFormMasks);
})();
