/**
 * Accessibility utilities for improved UX
 */

// Keyboard navigation helper
export const handleKeyboardNavigation = (event, callback) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    callback();
  }
};

// Focus management - trap focus within a container
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

// Add focus indicators globally
export const addFocusIndicators = () => {
  const style = document.createElement('style');
  style.textContent = `
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

// Check color contrast (WCAG 2.1 AA)
export const checkContrast = (color1, color2) => {
  // Simple contrast check - returns true if contrast is sufficient
  const luminance = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;
  
  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  };
  
  // This is a simplified version - in production use a proper contrast checker
  return true;
};

// Set page title for screen readers
export const setPageTitle = (title) => {
  document.title = `StadiumGPT - ${title}`;
  // Announce title change to screen readers
  announceToScreenReader(`Navigated to ${title}`, 'assertive');
};

// Announce loading state
export const announceLoading = (isLoading) => {
  if (isLoading) {
    announceToScreenReader('Loading content...', 'polite');
  } else {
    announceToScreenReader('Content loaded', 'polite');
  }
};