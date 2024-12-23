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

  async function createMessageElement(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${
      data.username === username ? 'user' : ''
    }`;

    const formattedTimestamp = formatTimestamp(data.timestamp);
    // Sanitize the username and message content
    const sanitizedUsername = DOMPurify.sanitize(data.username);
    const sanitizedMessage = DOMPurify.sanitize(data.message);

    // Filter profanity
    let censoredMessage = sanitizedMessage;
    try {
      const response = await fetch('/filter_profanity/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
        },
        body: sanitizedMessage,
      });
      const data = await response.json();
      censoredMessage = data.message;
    } catch (error) {
      console.error('Error filtering profanity:', error);
  }

    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="username">${sanitizedUsername}</span>
            <span class="timestamp">${formattedTimestamp}</span>
        </div>
        <div class="message-text">${censoredMessage}</div>
    `;

    return messageDiv;
  }

  // Function to display chat history
  async function displayChatHistory(history) {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = `
        <div style="height: 100%; display: flex; justify-content: center; align-items: center;">
          <div id="loading-messages" style="display: none;" class="message-loader"></div>
        </div>
      `; // Clear existing messages

    document.getElementById('loading-messages').style.display = 'block';

    for (const item of history.reverse()) {
      const messageElement = await createMessageElement(item);
      chatMessages.appendChild(messageElement);
    }

    document.getElementById('loading-messages').style.display = 'none';

    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Function to send message
    async function sendMessage() {
        const messageInput = document.getElementById('messageInput');
        let message = messageInput.value;
        message = DOMPurify.sanitize(message);

        const maxLength = 256;
        if (message.length > maxLength) {
            alert(`Message exceeds the ${maxLength} character limit.`);
            return;
        }

        if (message.trim() !== '') {
            const isValidSession = await validateSession();
            if (isValidSession) {
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
    }

    chatSocket.onmessage = async function (e) {
        const data = JSON.parse(e.data);

        if (data.error === 'Unauthorized') {
            alert('Your session has expired. Redirecting to login.');
            window.location.href = '/login/';
        } else if (data.history) {
          await displayChatHistory(data.history);
        } else if (data.message) {
            const chatMessages = document.getElementById('chat-messages');
            const messageElement = await createMessageElement(data);
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

    chatSocket.onclose = function (e) {
        if (e.code === 4001) { // Custom close code for logout
            //alert('Session expired. Redirecting ....');
            window.location.href = '/';
        } else {
            console.log('WebSocket closed:', e);
            const chatMessages = document.getElementById('chat-messages');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'chat-message error';
            errorDiv.textContent =
                'Your session has been terminated. Please refresh the page to reconnect.';
            chatMessages.appendChild(errorDiv);
        }
    };

  setTimeout(() => {
    document
      .getElementById('messageInput')
      .addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          sendMessage();
        }
      });
    const sendButton = document.getElementById('send-message');
    if (sendButton) {
      sendButton.addEventListener('click', sendMessage);
    }
  });
}


async function validateSession() {
    try {
        const response = await fetch('/validate_session/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        });

        if (response.ok) {
            const data = await response.json();
            return data.authenticated;
        } else if (response.status === 401) {
            alert('Your session has expired. Logging you out');
            window.location.href = '/';
            return false;
        } else {
            console.error('Unexpected response:', response);
            return false;
        }
    } catch (error) {
        console.error('Error validating session:', error);
        return false;
    }
}


function checkProfanity() {
  const messageInput = document.getElementById('messageInput').value;
  
  fetch('/check_profanity/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
    },
    body: messageInput,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        const profanityWarning = document.getElementById('profanity-warning');

        if (data.value == 1) {
          profanityWarning.style.display = 'block';
        } else {
          profanityWarning.style.display = 'none';
        }
      }
    })
    .catch((error) => {
      console.log('Error checking message profanity:', error);
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
            <div class="chat-input-row">
              <input type="text" id="messageInput" placeholder="Type a message..." autocomplete="off" maxlength="256" onkeyup="updateCharacterCount(); checkProfanity()">
              <button id="send-message">Send</button>
            </div>
            <div id="charCount" style="font-size: 0.9em; color: #666;">256 characters remaining</div>
            <div id="profanity-warning" style="display: none; color: red; font-size: 1em; margin-top: 5px;">Warning: This message may contain inappropriate content</div>
        </div>
    </div>`;
}

function updateCharacterCount() {
  const maxChars = 256;
  const messageInput = document.getElementById('messageInput');
  const charCount = document.getElementById('charCount');
  const remaining = maxChars - messageInput.value.length;

  charCount.textContent = `${remaining} characters remaining`;

  if (remaining < 0) {
    charCount.style.color = 'red';
  } else {
    charCount.style.color = '#666';
  }
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
            <input type="text" placeholder="Type a message..." autocomplete="off" disabled>
            <button disabled>Send</button>
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
