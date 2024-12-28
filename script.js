document.addEventListener('DOMContentLoaded', function() {
    const studentForm = document.getElementById('studentForm');
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    let studentData = null;

    // Handle form submission
    studentForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        studentData = {
            fullName: document.getElementById('fullName').value,
            age: document.getElementById('age').value,
            educationLevel: document.getElementById('educationLevel').value,
            course: document.getElementById('course').value,
            income: document.getElementById('income').value,
            category: document.getElementById('category').value,
            state: document.getElementById('state').value,
            percentage: document.getElementById('percentage').value,
            aadhar: document.getElementById('aadhar').value,
            email: document.getElementById('email').value
        };

        try {
            const response = await fetch('/submit-info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(studentData)
            });

            const data = await response.json();
            if (data.status === 'success') {
                showMessage('Information submitted successfully! You can now ask questions about scholarships and opportunities.', 'system');
                studentForm.style.display = 'none';
            } else {
                showMessage('Error submitting information. Please try again.', 'error');
            }
        } catch (error) {
            showMessage('Error submitting information. Please try again.', 'error');
        }
    });

    // Handle sending messages
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    window.sendMessage = async function() {
        if (!studentData) {
            showMessage('Please submit your information first.', 'error');
            return;
        }

        const message = userInput.value.trim();
        if (!message) return;

        showMessage(message, 'user');
        userInput.value = '';
        addTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    studentInfo: studentData
                })
            });

            const data = await response.json();
            removeTypingIndicator();

            if (data.status === 'success') {
                showMessage(data.response, 'assistant');
            } else {
                showMessage('Error getting response. Please try again.', 'error');
            }
        } catch (error) {
            removeTypingIndicator();
            showMessage('Error getting response. Please try again.', 'error');
        }
    }

    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (type === 'assistant') {
            contentDiv.innerHTML = message;
        } else {
            contentDiv.textContent = message;
        }

        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function addTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator assistant-message';
        indicator.id = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        chatContainer.appendChild(indicator);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
});
