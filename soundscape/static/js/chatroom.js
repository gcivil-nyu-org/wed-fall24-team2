function getChatroomComponent(neighborhood) {
  return `<div class="chat-container">
        <div class="chat-header">
            ${neighborhood.name}
        </div>
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
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Type a message..." autocomplete="off" onkeydown="checkEnter(event)">
            <button id='send-message' onclick="sendMessage()">Send</button>
        </div>
    </div>`;
}

function getCurrentTime() {
  const now = new Date();
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  };
  return now.toLocaleString('en-US', options);
}

function sendMessage() {
  const input = document.getElementById('messageInput');
  const message = input.value.trim();

  if (message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', 'user');

    const headerDiv = document.createElement('div');
    headerDiv.classList.add('message-header');

    const usernameSpan = document.createElement('span');
    usernameSpan.classList.add('username');
    usernameSpan.textContent = 'You'; // Mocked as "You"

    const timestampSpan = document.createElement('span');
    timestampSpan.classList.add('timestamp');
    timestampSpan.textContent = getCurrentTime();

    headerDiv.appendChild(usernameSpan);
    headerDiv.appendChild(timestampSpan);

    const messageText = document.createElement('div');
    messageText.classList.add('message-text');
    messageText.textContent = message;

    messageDiv.appendChild(headerDiv);
    messageDiv.appendChild(messageText);

    const deleteBtn = document.createElement('button');
    deleteBtn.classList.add('delete-btn');
    deleteBtn.textContent = '×';
    deleteBtn.onclick = function () {
      deleteMessage(messageDiv);
    };
    messageDiv.appendChild(deleteBtn);
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
      chatMessages.appendChild(messageDiv);
      input.value = '';
      // Scroll to the latest message
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }
}

function deleteMessage(messageElement) {
  const chatMessages = document.getElementById('chat-messages');
  if (chatMessages) {
    chatMessages.removeChild(messageElement);
  }
}

// Function to check for Enter key press
function checkEnter(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
}
