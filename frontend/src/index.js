import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';
import { addFocusIndicators, announcePageLoad } from './utils/accessibility';

// Add accessibility features
addFocusIndicators();
announcePageLoad();

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* ✅ Skip to main content link - improves accessibility score */}
    <a href="#main-content" className="skip-to-content">
      Skip to main content
    </a>
    <App />
  </React.StrictMode>
);