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
    $('#send_button').on('click', function (e) {
        const message = $('#msg_input').val();
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
    });

    // Send message on Enter key press
    $(document).ready(function() {
        $('#msg_input').keydown(function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                $('#send_button').click();
            }
        });
    });

    // Update the session ID on page load if it exists in sessionStorage
    $(window).on('load', function () {
        const sessionId = sessionStorage.getItem('session_id') || createSessionId();
        updateSessionId(sessionId);  // Display the session ID when the page loads
        showBotMessage('Hello there! Type in a message.');
    });
