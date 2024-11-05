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

function getChatroomPublicComponent(neighborhood) {
  return `
    <div class="chat-container">
        <div id="room-name" class="chat-header">
            ${neighborhood.name}
        </div>
        <div class="chat-messages-wrapper" style="position: relative;">
            <div class="chat-messages" id="chat-messages">
                <!-- Preloaded messages -->
                <div class="chat-message">
                    <div class="message-header">
                        <span class="username">Alice</span>
                        <span class="timestamp">10/10/2024 10:30 AM</span>
                    </div>
                    <div class="message-text">Hi all, I'm thinking of moving to this neighborhood, how is the noise like at night?</div>
                </div>
                <div class="chat-message user">
                    <div class="message-header">
                        <span class="username">John</span>
                        <span class="timestamp">10/10/2024 10:32 AM</span>
                    </div>
                    <div class="message-text">It's pretty quiet at night.</div>
                </div>
                <div class="chat-message">
                    <div class="message-header">
                        <span class="username">Bob</span>
                        <span class="timestamp">10/10/2024 10:35 AM</span>
                    </div>
                    <div class="message-text">I heard some construction on ${neighborhood.nearbyStreet} last week but that was during the day.</div>
                </div>
            </div>
            <!-- Login overlay -->
            <div class="chat-overlay">
                <div class="overlay-content">
                    <h3>Join the Conversation</h3>
                    <p>Please sign up or log in to participate in this chat</p>
                    <button onclick="window.location.href='/signup'" class="signup-button">Signup</button>
                    <button onclick="window.location.href='/login'" class="login-button">Login</button>
                </div>
            </div>
        </div>
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Type a message..." autocomplete="off" disabled>
            <button id="send-message" onclick="sendMessage()" disabled>Send</button>
        </div>
    </div>
    <style>
        .chat-messages-wrapper {
            position: relative;
            height: 400px;
        }

        .chat-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .overlay-content {
            text-align: center;
            padding: 20px;
            margin-bottom: 40px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }

        .overlay-content h3 {
            margin: 0 0 10px 0;
            color: #333;
        }

        .overlay-content p {
            margin: 0 0 20px 0;
            color: #666;
        }

        .login-button, .signup-button {
            background: #a527cf;
            color: white;
            border: none;
            padding: 5px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }

        /* Disabled input styling */
        input:disabled, button:disabled {
            background-color: #f5f5f5;
            cursor: not-allowed;
        }
    </style>`;
}
