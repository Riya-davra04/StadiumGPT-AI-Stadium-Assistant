/**
 * Accessibility utilities for improved UX
 */

// Screen reader announcements
export const announceToScreenReader = (message, politeness = 'polite') => {
  const announcement = document.createElement('div');
  announcement.setAttribute('aria-live', politeness);
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';
  announcement.textContent = message;
  document.body.appendChild(announcement);
  
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 5000);
};

// Keyboard navigation helper
export const handleKeyboardNavigation = (event, callback) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    callback();
  }
};

// Focus trap for modals
export const focusTrap = (element, event) => {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  if (focusableElements.length === 0) return;
  
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];
  
  if (event.key === 'Tab') {
    if (event.shiftKey && document.activeElement === firstElement) {
      event.preventDefault();
      lastElement.focus();
    } else if (!event.shiftKey && document.activeElement === lastElement) {
      event.preventDefault();
      firstElement.focus();
    }
  }
};

// Add global focus indicators
export const addFocusIndicators = () => {
  const style = document.createElement('style');
  style.textContent = `
    /* Skip to main content link */
    .skip-to-content {
      position: absolute;
      top: -40px;
      left: 0;
      background: #1976D2;
      color: white;
      padding: 8px 16px;
      z-index: 1000;
      text-decoration: none;
      border-radius: 0 0 4px 4px;
    }
    
    .skip-to-content:focus {
      top: 0;
    }
    
    /* Focus indicators */
    :focus {
      outline: 3px solid #1976D2 !important;
      outline-offset: 2px !important;
    }
    
    :focus:not(:focus-visible) {
      outline: none !important;
    }
    
    :focus-visible {
      outline: 3px solid #1976D2 !important;
      outline-offset: 2px !important;
    }
    
    /* Screen reader only */
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    
    /* High contrast focus */
    .high-contrast :focus-visible {
      outline: 4px solid #000 !important;
    }
  `;
  document.head.appendChild(style);
};

// Announce page load
export const announcePageLoad = () => {
  announceToScreenReader('StadiumGPT application loaded', 'assertive');
};

// Set page title
export const setPageTitle = (title) => {
  document.title = `StadiumGPT - ${title}`;
  announceToScreenReader(`Navigated to ${title}`, 'assertive');
};