// Function to get the current timestamp
function getCurrentTimestamp() {
    return new Date();
}

// Renders the message on the chat window
function renderMessageToScreen(args) {
    let displayDate = (args.time || getCurrentTimestamp()).toLocaleString('en-IN', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
    });
    let messagesContainer = $('.messages');

    // Create the message HTML
    let message = $(`
        <li class="message ${args.message_side}">
            <div class="avatar"></div>
            <div class="text_wrapper">
                <div class="text">${args.text}</div>
                <div class="timestamp">${displayDate}</div>
            </div>
        </li>
    `);

    // Append the message to the chat window
    messagesContainer.append(message);

    // Animate message appearance
    setTimeout(function () {
        message.addClass('appeared');
    }, 0);
    messagesContainer.animate({ scrollTop: messagesContainer.prop('scrollHeight') }, 300);
}

// Sends the user message to the chat window
function showUserMessage(message, datetime) {
    renderMessageToScreen({
        text: message,
        time: datetime,
        message_side: 'right',
    });
}

// Sends the bot message to the chat window
function showBotMessage(message, datetime) {
    renderMessageToScreen({
        text: message,
        time: datetime,
        message_side: 'left',
    });
}

// Generate a session ID or get from sessionStorage
function createSessionId() {
    const sessionId = 'session-' + Date.now();
    sessionStorage.setItem('session_id', sessionId);
    return sessionId;
}

// Function to update the session ID in the top_menu
function updateSessionId(sessionId) {
    $('.top_menu .title').text(`Session: ${sessionId}`);  // Update the session ID in the title
}

// Event listener for send button
$('#send_button').on('click', function () {
    const message = $('#msg_input').val();
    sendMessage(message);
});

// Send message on Enter key press
$(document).ready(function () {
    $('#msg_input').keydown(function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            $('#send_button').click();
        }
    });
});

// Voice input function
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US';

// Event listener for voice button
$('#voice_button').on('click', function () {
    recognition.start();
});

// Handle voice input and send automatically
recognition.onresult = function (event) {
    let transcript = event.results[0][0].transcript;
    $('#msg_input').val(transcript);
    sendMessage(transcript);  // Automatically send the message
};

// Handle errors
recognition.onerror = function (event) {
    console.error("Speech recognition error:", event.error);
    showBotMessage("Sorry, I couldn't hear you. Please try again.");
};

// Function to send a message
function sendMessage(message) {
    const sessionId = sessionStorage.getItem('session_id') || createSessionId();

    if (!message.trim()) {
        alert("Please enter a message!");  // Prevent sending empty input
        return;
    }

    showUserMessage(message);
    $('#msg_input').val(''); // Clear input

    // Send user input to backend for response
    $.ajax({
        url: '/get_response',  // Send request to /get_response
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ prompt: message, session_id: sessionId }),
        success: function (response) {
            showBotMessage(response.response);  // Display bot response
            updateSessionId(response.session_id);  // Update session ID in top_menu
        },
        error: function (xhr, status, error) {
            console.error("Error: " + error); // Log the error for debugging
            showBotMessage('Error communicating with the bot.');
        }
    });
}

// Update the session ID on page load if it exists in sessionStorage
$(window).on('load', function () {
    const sessionId = sessionStorage.getItem('session_id') || createSessionId();
    updateSessionId(sessionId);  // Display the session ID when the page loads
    showBotMessage("Welcome! This is Your Personal Assistant. How can I help you?");
    loadUserProfile();
});
// Fetch user profile from JSON
function loadUserProfile() {
    $.getJSON('/static/user.json', function (data) {
        $('#profile-name').text(data.name);
        $('#profile-fullname').text("Full Name: " + data.full_name);
        $('#profile-email').text("Email: " + data.email);
        $('#profile-phone').text("Phone: " + data.phone);
        if (data.profile_pic) {
            $('#profile-pic').css('background-image', `url('${data.profile_pic}')`);
        }
    }).fail(function () {
        console.error("Failed to load user profile.");
    });

    // Toggle expand/collapse on click
    $('#user-profile').on('click', function () {
        $(this).toggleClass('expanded');
    });
}

