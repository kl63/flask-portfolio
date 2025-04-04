// chat.js - You can create this file in your static/js folder and include it in your layout if you want to keep chat scripts separate

document.addEventListener('DOMContentLoaded', function() {
    const chatButton = document.getElementById('chat-button');
    const chatContainer = document.getElementById('chat-container');
    const closeChat = document.getElementById('close-chat');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicator = document.getElementById('typing-indicator');
    
    // Toggle chat container visibility
    chatButton.addEventListener('click', function() {
      chatContainer.style.display = chatContainer.style.display === 'none' || chatContainer.style.display === '' ? 'flex' : 'none';
      if (chatContainer.style.display === 'flex') {
        chatInput.focus();
      }
    });
    
    closeChat.addEventListener('click', function() {
      chatContainer.style.display = 'none';
    });
    
    // Send message function
    function sendMessage() {
      const message = chatInput.value.trim();
      if (message.length === 0) return;
      
      // Add user message to chat
      const userMessageElement = document.createElement('div');
      userMessageElement.classList.add('message', 'user-message');
      userMessageElement.textContent = message;
      chatMessages.appendChild(userMessageElement);
      
      // Clear input
      chatInput.value = '';
      
      // Scroll to bottom
      chatMessages.scrollTop = chatMessages.scrollHeight;
      
      // Show typing indicator
      typingIndicator.style.display = 'flex';
      
      // Send message to server
      fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
      })
      .then(response => response.json())
      .then(data => {
        // Hide typing indicator
        typingIndicator.style.display = 'none';
        
        // Add bot message to chat
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot-message');
        botMessageElement.textContent = data.response;
        chatMessages.appendChild(botMessageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
      })
      .catch(error => {
        console.error('Error:', error);
        typingIndicator.style.display = 'none';
        
        // Add error message
        const errorMessageElement = document.createElement('div');
        errorMessageElement.classList.add('message', 'bot-message');
        errorMessageElement.textContent = 'Sorry, something went wrong. Please try again later.';
        chatMessages.appendChild(errorMessageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
      });
    }
    
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on enter key press
    chatInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
    
    // Store chat history in localStorage to persist across page refreshes (optional)
    function saveChat() {
      const messages = chatMessages.innerHTML;
      localStorage.setItem('chatHistory', messages);
    }
    
    function loadChat() {
      const savedChat = localStorage.getItem('chatHistory');
      if (savedChat) {
        chatMessages.innerHTML = savedChat;
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }
    }
    
    // Uncomment these lines if you want to save chat history
    // window.addEventListener('beforeunload', saveChat);
    // loadChat();
  });