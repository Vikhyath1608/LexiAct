let sessionId = null;  // To store session ID

document.querySelector("#send").addEventListener("click", function() {
    let userInput = document.querySelector("#user-input").value;

    if (userInput.trim() !== "") {
        // Display the user's input in the chat box
        let chatBox = document.querySelector("#chat-box");
        chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
        document.querySelector("#user-input").value = "";  // Clear input

        // Send the user input to the backend
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userInput, session_id: sessionId })
        })
        .then(response => response.json())
        .then(data => {
            // Display the AI response in the chat box
            chatBox.innerHTML += `<p><strong>AI:</strong> ${data.response}</p>`;
            chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message

            // Save the session ID to maintain conversation continuity
            sessionId = data.session_id;
        })
        .catch(error => console.error("Error:", error));
    }
});
