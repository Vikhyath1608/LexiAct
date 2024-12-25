const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const chatMessages = document.querySelector('.chat-messages');

// Add a function to scroll the chat messages to the bottom
function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendButton.addEventListener('click', () => {
  const userInput = messageInput.value;
  if (userInput.trim() !== '') {
    // Add user's message to the chat history
    chatMessages.innerHTML += `<div class="user-message">${userInput}</div>`;

    // Simulate a bot response (replace with your actual chatbot logic)
    const botResponse = "Hello there!";
    chatMessages.innerHTML += `<div class="bot-message">${botResponse}</div>`;

    messageInput.value = '';
    scrollToBottom();
  }
});