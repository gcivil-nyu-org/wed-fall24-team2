// Initialize WebSocket and chat functionality
function initializeChat(neighborhood) {
  const boxName = encodeURIComponent(neighborhood.name.replace(/-/g, ' '));
  const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chatroom/' + boxName + '/'
  );


function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
    };
    return date.toLocaleString(undefined, options);
}

function createMessageElement(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${
      data.username === username ? 'user' : ''
    }`;

    const formattedTimestamp = formatTimestamp(data.timestamp);

    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="username">${data.username}</span>
            <span class="timestamp">${formattedTimestamp}</span>
        </div>
        <div class="message-text">${data.message}</div>
    `;

    return messageDiv;
}
  // Function to display chat history
  function displayChatHistory(history) {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = ''; // Clear existing messages

    history.forEach((item) => {
      const messageElement = createMessageElement(item);
      chatMessages.appendChild(messageElement);
    });

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Function to send message
  function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value;
    if (message.trim() !== '') {
      const timestamp = new Date().toISOString();
      chatSocket.send(
        JSON.stringify({
          message,
          username,
          timestamp,
        })
      );
      messageInput.value = '';
    }
  }

  // Handle incoming WebSocket messages
  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const chatMessages = document.getElementById('chat-messages');

    if (data.history) {
      displayChatHistory(data.history);
    } else if (data.message) {
      const messageElement = createMessageElement(data);
      chatMessages.appendChild(messageElement);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  };

  // Handle WebSocket connection errors
  chatSocket.onerror = function (error) {
    console.error('WebSocket Error:', error);
    const chatMessages = document.getElementById('chat-messages');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'chat-message error';
    errorDiv.textContent =
      'Error: Could not connect to chat server. Please try refreshing the page.';
    chatMessages.appendChild(errorDiv);
  };

  // Handle WebSocket disconnection
  chatSocket.onclose = function (e) {
    console.log('Chat socket closed unexpectedly');
    const chatMessages = document.getElementById('chat-messages');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'chat-message error';
    errorDiv.textContent =
      'Connection lost. Please refresh the page to reconnect.';
    chatMessages.appendChild(errorDiv);
  };

  document
    .getElementById('messageInput')
    .addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
      }
    });
}

function getChatroomComponent(neighborhood) {
  return `
    <div class="chat-container">
        <div id="room-name" class="chat-header">
            ${neighborhood.name}
        </div>
        <div class="chat-messages" id="chat-messages">
        </div>
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Type a message..." autocomplete="off">
            <button id="send-message" onclick="sendMessage()">Send</button>
        </div>
    </div>`;
}
