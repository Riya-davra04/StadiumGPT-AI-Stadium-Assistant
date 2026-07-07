import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  CircularProgress,
  Avatar,
  Chip,
  Zoom,
  Fade,
  LinearProgress,
} from '@mui/material';
import {
  Send,
  Mic,
  Close,
  SmartToy,
  Person,
  VolumeUp,
  VolumeOff,
  Refresh,
} from '@mui/icons-material';
import { useWebSocket } from '../context/WebSocketContext';
import { useAuth } from '../context/AuthContext';

const ChatAssistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const { sendMessage, messages: wsMessages, isConnected } = useWebSocket();
  const { user } = useAuth();

  const suggestedQuestions = [
    'How to reach Gate B?',
    'Food queue status?',
    'Nearest restroom?',
    'Crowd information',
    'Emergency contact?',
    'Accessible routes?',
    'Transport options?',
  ];

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (wsMessages.length > 0) {
      const lastMessage = wsMessages[wsMessages.length - 1];
      if (lastMessage.type === 'ai_response' || lastMessage.type === 'chat') {
        setMessages(prev => [...prev, {
          text: lastMessage.content || lastMessage.text || 'Response received',
          sender: 'ai',
          timestamp: new Date(),
        }]);
        setIsLoading(false);
      }
    }
  }, [wsMessages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading || !isConnected) return;

    const userMessage = {
      text: input,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const query = input;
    setInput('');
    setIsLoading(true);

    try {
      await sendMessage('chat', {
        content: query,
        userId: user?.id || 'guest',
        context: {
          stadium: 'FIFA World Cup Stadium',
          language: user?.language || 'English',
          section: user?.preferences?.favorite_sections?.[0] || '',
        },
      });
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'ai',
        timestamp: new Date(),
        error: true,
      }]);
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Voice recognition is not supported in this browser.');
      return;
    }

    const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = user?.language === 'Hindi' ? 'hi-IN' : 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    setIsListening(true);

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
      setIsListening(false);
      // Auto-send after voice input
      setTimeout(handleSend, 500);
    };

    recognition.onerror = () => {
      setIsListening(false);
      toast.error('Voice recognition failed. Please try again.');
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  const handleSpeak = (text) => {
    if (!('speechSynthesis' in window)) {
      alert('Text-to-speech is not supported in this browser.');
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 1;
    utterance.pitch = 1;
    
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  return (
    <>
      {!isOpen && (
        <Zoom in={!isOpen}>
          <Box
            position="fixed"
            bottom={24}
            right={24}
            zIndex={1000}
          >
            <IconButton
              color="primary"
              onClick={() => setIsOpen(true)}
              sx={{
                width: 64,
                height: 64,
                bgcolor: 'primary.main',
                color: 'white',
                '&:hover': {
                  bgcolor: 'primary.dark',
                  transform: 'scale(1.05)',
                },
                boxShadow: '0 4px 20px rgba(25, 118, 210, 0.4)',
                transition: 'all 0.2s',
              }}
            >
              <SmartToy sx={{ fontSize: 32 }} />
            </IconButton>
          </Box>
        </Zoom>
      )}

      {isOpen && (
        <Zoom in={isOpen}>
          <Paper
            elevation={8}
            sx={{
              position: 'fixed',
              bottom: 24,
              right: 24,
              width: { xs: 'calc(100% - 32px)', sm: 400 },
              height: { xs: 'calc(100% - 100px)', sm: 580 },
              display: 'flex',
              flexDirection: 'column',
              borderRadius: 3,
              overflow: 'hidden',
              zIndex: 1000,
              bgcolor: 'background.paper',
              maxWidth: 450,
              boxShadow: '0 8px 40px rgba(0,0,0,0.15)',
            }}
          >
            {/* Header */}
            <Box
              sx={{
                p: 2,
                bgcolor: 'primary.main',
                color: 'white',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexShrink: 0,
              }}
            >
              <Box display="flex" alignItems="center" gap={1.5}>
                <SmartToy />
                <Box>
                  <Typography variant="h6" fontWeight="bold" fontSize="1rem">
                    StadiumGPT Assistant
                  </Typography>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Box
                      sx={{
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        bgcolor: isConnected ? 'success.main' : 'error.main',
                      }}
                    />
                    <Typography variant="caption" sx={{ opacity: 0.8 }}>
                      {isConnected ? 'Online' : 'Connecting...'}
                    </Typography>
                  </Box>
                </Box>
              </Box>
              <IconButton
                size="small"
                onClick={() => setIsOpen(false)}
                sx={{ color: 'white', '&:hover': { bgcolor: 'rgba(255,255,255,0.1)' } }}
              >
                <Close />
              </IconButton>
            </Box>

            {/* Messages */}
            <Box
              sx={{
                flex: 1,
                overflowY: 'auto',
                p: 2,
                bgcolor: 'grey.50',
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              {messages.length === 0 ? (
                <Box
                  display="flex"
                  flexDirection="column"
                  alignItems="center"
                  justifyContent="center"
                  height="100%"
                  gap={2}
                  sx={{ opacity: 0.6 }}
                >
                  <SmartToy sx={{ fontSize: 56, color: 'grey.400' }} />
                  <Typography color="text.secondary" align="center" variant="body2">
                    Hi! I'm StadiumGPT Assistant.
                    <br />
                    Ask me anything about the stadium!
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1} justifyContent="center" sx={{ mt: 1 }}>
                    {suggestedQuestions.slice(0, 4).map(suggestion => (
                      <Chip
                        key={suggestion}
                        label={suggestion}
                        onClick={() => {
                          setInput(suggestion);
                          setTimeout(handleSend, 200);
                        }}
                        clickable
                        variant="outlined"
                        size="small"
                        sx={{ maxWidth: '100%' }}
                      />
                    ))}
                  </Box>
                </Box>
              ) : (
                <>
                  {messages.map((message, index) => (
                    <Box
                      key={index}
                      display="flex"
                      justifyContent={message.sender === 'user' ? 'flex-end' : 'flex-start'}
                      mb={1.5}
                      sx={{
                        animation: 'fadeIn 0.3s ease-out',
                      }}
                    >
                      <Box
                        display="flex"
                        gap={1}
                        alignItems="flex-start"
                        maxWidth="85%"
                      >
                        {message.sender === 'ai' && (
                          <Avatar sx={{ width: 28, height: 28, bgcolor: 'primary.main' }}>
                            <SmartToy sx={{ fontSize: 14 }} />
                          </Avatar>
                        )}
                        <Box>
                          <Paper
                            elevation={0}
                            sx={{
                              p: 1.5,
                              bgcolor: message.sender === 'user' ? 'primary.main' : 'white',
                              color: message.sender === 'user' ? 'white' : 'text.primary',
                              borderRadius: message.sender === 'user' 
                                ? '16px 16px 4px 16px' 
                                : '16px 16px 16px 4px',
                              border: message.sender === 'ai' ? '1px solid #e0e0e0' : 'none',
                              wordBreak: 'break-word',
                            }}
                          >
                            <Typography variant="body2" sx={{ fontSize: '0.9rem' }}>
                              {message.text}
                            </Typography>
                          </Paper>
                          <Box display="flex" alignItems="center" gap={1} mt={0.5}>
                            <Typography variant="caption" color="text.secondary">
                              {message.timestamp?.toLocaleTimeString()}
                            </Typography>
                            {message.sender === 'ai' && (
                              <IconButton
                                size="small"
                                onClick={() => handleSpeak(message.text)}
                                sx={{ p: 0.5 }}
                              >
                                {isSpeaking ? <VolumeOff fontSize="small" /> : <VolumeUp fontSize="small" />}
                              </IconButton>
                            )}
                          </Box>
                        </Box>
                        {message.sender === 'user' && (
                          <Avatar sx={{ width: 28, height: 28, bgcolor: 'grey.400' }}>
                            <Person sx={{ fontSize: 14 }} />
                          </Avatar>
                        )}
                      </Box>
                    </Box>
                  ))}
                  {isLoading && (
                    <Box display="flex" justifyContent="flex-start" mb={1.5}>
                      <Box display="flex" alignItems="center" gap={1}>
                        <Avatar sx={{ width: 28, height: 28, bgcolor: 'primary.main' }}>
                          <SmartToy sx={{ fontSize: 14 }} />
                        </Avatar>
                        <Box>
                          <Paper
                            elevation={0}
                            sx={{
                              p: 1.5,
                              bgcolor: 'white',
                              borderRadius: '16px 16px 16px 4px',
                              border: '1px solid #e0e0e0',
                            }}
                          >
                            <Box display="flex" alignItems="center" gap={2}>
                              <CircularProgress size={20} />
                              <Typography variant="body2" color="text.secondary">
                                Thinking...
                              </Typography>
                            </Box>
                          </Paper>
                        </Box>
                      </Box>
                    </Box>
                  )}
                  <div ref={messagesEndRef} />
                </>
              )}
            </Box>

            {/* Input */}
            <Box
              sx={{
                p: 2,
                borderTop: 1,
                borderColor: 'grey.200',
                bgcolor: 'background.paper',
                flexShrink: 0,
              }}
            >
              <Box display="flex" gap={1}>
                <TextField
                  fullWidth
                  size="small"
                  placeholder="Ask me anything..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  disabled={isLoading || !isConnected}
                  inputRef={inputRef}
                  InputProps={{
                    sx: { 
                      bgcolor: 'grey.50',
                      borderRadius: 2,
                      '& .MuiOutlinedInput-notchedOutline': {
                        borderColor: 'grey.300',
                      },
                    },
                  }}
                />
                <IconButton
                  onClick={handleVoiceInput}
                  color={isListening ? 'error' : 'default'}
                  disabled={isLoading || !isConnected}
                  sx={{
                    bgcolor: isListening ? 'error.light' : 'transparent',
                    '&:hover': {
                      bgcolor: isListening ? 'error.light' : 'grey.100',
                    },
                  }}
                >
                  <Mic />
                </IconButton>
                <IconButton
                  color="primary"
                  onClick={handleSend}
                  disabled={!input.trim() || isLoading || !isConnected}
                  sx={{
                    bgcolor: 'primary.main',
                    color: 'white',
                    '&:hover': {
                      bgcolor: 'primary.dark',
                    },
                    '&.Mui-disabled': {
                      bgcolor: 'grey.300',
                      color: 'grey.500',
                    },
                  }}
                >
                  <Send />
                </IconButton>
              </Box>
              {!isConnected && (
                <Box mt={1}>
                  <LinearProgress />
                  <Typography variant="caption" color="text.secondary">
                    Connecting to server...
                  </Typography>
                </Box>
              )}
            </Box>
          </Paper>
        </Zoom>
      )}
    </>
  );
};

export default ChatAssistant;