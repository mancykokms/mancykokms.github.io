CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .gradio-container {
    font-family: 'Inter', system-ui, sans-serif !important;
}

.gradio-container {
    max-width: 820px !important;
    margin: 0 auto !important;
    padding: 2rem 1rem 1rem !important;
}

/* Title gradient */
.gradio-container h1 {
    background: linear-gradient(135deg, #6C63FF, #a855f7) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 700 !important;
    font-size: 2.2rem !important;
    text-align: center !important;
    letter-spacing: -0.02em !important;
}

/* Chatbot container */
.chatbot, [data-testid="chatbot"] {
    border-radius: 16px !important;
    min-height: 400px !important;
}

/* Bubble shapes */
.bot .message-bubble-border {
    border-radius: 18px 18px 18px 4px !important;
}

.user .message-bubble-border {
    border-radius: 18px 18px 4px 18px !important;
}

/* Text inside bubbles */
.message-bubble-border p,
.message-bubble-border li,
.message-bubble-border h1,
.message-bubble-border h2,
.message-bubble-border h3 {
    color: inherit !important;
    line-height: 1.65 !important;
    text-align: left !important;
}

/* Input */
textarea {
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    resize: none !important;
}

/* Examples — compact pill row */
.examples table, .examples tbody, .examples tr {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    border: none !important;
    background: transparent !important;
}

.examples td {
    display: block !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
}

.examples button {
    border-radius: 20px !important;
    font-size: 0.82rem !important;
    padding: 6px 14px !important;
    white-space: nowrap !important;
    height: auto !important;
    min-height: unset !important;
    transition: transform 0.2s ease !important;
}

.examples button:hover {
    transform: translateY(-1px) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #6C63FF55; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #6C63FF; }
"""

JS = """
function() {
    const container = document.querySelector('.gradio-container');
    if (container) {
        container.style.opacity = '0';
        container.style.transform = 'translateY(16px)';
        requestAnimationFrame(() => {
            container.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        });
    }
}
"""

EXAMPLES = [
    "What's your background?",
    "What tech do you work with?",
    "Tell me about your projects",
    "What roles are you open to?",
    "AI / ML experience?",
    "I'd like to get in touch",
]
