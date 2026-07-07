// frontend/src/utils/websocket.js
export const setupWebSocket = (onMessage) => {
  const ws = new WebSocket('ws://localhost:8000/ws/dashboard');
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'crowd_update') {
      onMessage(data);
    }
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  return ws;
};