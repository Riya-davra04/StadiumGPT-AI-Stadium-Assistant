import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Toaster } from 'react-hot-toast';
import theme from './theme';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Navigation from './pages/Navigation';
import CrowdMap from './pages/CrowdMap';
import Queues from './pages/Queues';
import Emergency from './pages/Emergency';
import Accessibility from './pages/Accessibility';
import Transport from './pages/Transport';
import ChatAssistant from './components/ChatAssistant';
import { WebSocketProvider } from './context/WebSocketContext';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <WebSocketProvider>
          <Router>
            <div className="min-h-screen bg-gray-50">
              <Navbar />
              <main className="container-custom py-6">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/navigation" element={<Navigation />} />
                  <Route path="/crowd-map" element={<CrowdMap />} />
                  <Route path="/queues" element={<Queues />} />
                  <Route path="/emergency" element={<Emergency />} />
                  <Route path="/accessibility" element={<Accessibility />} />
                  <Route path="/transport" element={<Transport />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </main>
              <ChatAssistant />
            </div>
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#fff',
                  color: '#1a1a1a',
                  borderRadius: '12px',
                  padding: '16px 20px',
                },
              }}
            />
          </Router>
        </WebSocketProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;