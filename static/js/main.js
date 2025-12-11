const menuButton = document.getElementById('menu-button');
const mobileMenu = document.getElementById('mobile-menu');
const body = document.body;

if (menuButton && mobileMenu) {
  menuButton.addEventListener('click', () => {
    const isOpen = mobileMenu.classList.contains('hidden');
    mobileMenu.classList.toggle('hidden');
    menuButton.setAttribute('aria-expanded', String(isOpen));
    body.classList.toggle('nav-open');
  });
}

function handleFormValidation(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', (event) => {
    const invalid = [...form.querySelectorAll('[required]')].filter((input) => !input.value.trim());
    if (invalid.length > 0) {
      event.preventDefault();
      invalid[0].focus();
      const message = form.querySelector('.client-error');
      if (message) {
        message.textContent = 'Please fill out all required fields before submitting.';
      }
    }
  });
}

handleFormValidation('contact-form');
handleFormValidation('application-form');
