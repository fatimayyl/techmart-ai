(function () {
    'use strict';

    let sessionId = null;
    let isLoading = false;

    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const clearChat = document.getElementById('clear-chat');
    const welcomeContainer = document.getElementById('welcome-container');
    const headerStatus = document.getElementById('header-status');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');

    let typingEl = null;

    function createTypingIndicator() {
        const div = document.createElement('div');
        div.className = 'typing-indicator';
        div.innerHTML = `
            <div class="typing-row" style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
                <div class="msg-avatar">🤖</div>
                <div class="typing-bubble" style="background:#f0f0f0; padding:10px; border-radius:10px;">...</div>
            </div>
        `;
        return div;
    }

    function showTyping() {
        if (!typingEl) typingEl = createTypingIndicator();
        if (chatMessages) chatMessages.appendChild(typingEl);
        scrollToBottom();
        if (headerStatus) {
            headerStatus.textContent = 'Yazıyor...';
            headerStatus.style.color = '#f39c12';
        }
    }

    function hideTyping() {
        if (typingEl && typingEl.parentNode) typingEl.parentNode.removeChild(typingEl);
        if (headerStatus) {
            headerStatus.textContent = 'Çevrimiçi';
            headerStatus.style.color = '#2ecc71';
        }
    }

    function getTime() {
        return new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
    }

    function formatBotMessage(text) {
        return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
    }

    function addMessage(content, role, toolsUsed) {
        if (welcomeContainer) welcomeContainer.style.display = 'none';
        if (!chatMessages) return;

        const row = document.createElement('div');
        row.className = `message-row ${role}`; // Sadece class atıyoruz

        const bubble = document.createElement('div');
        bubble.className = 'msg-bubble'; // Renkleri CSS'ten alacak

        if (role === 'bot') bubble.innerHTML = formatBotMessage(content);
        else bubble.textContent = content;

        row.appendChild(bubble);
        chatMessages.appendChild(row);
        scrollToBottom();
    }

    function scrollToBottom() {
        if (chatMessages) {
            requestAnimationFrame(() => {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            });
        }
    }

    async function sendMessage(message) {
        if (isLoading || !message.trim()) return;
        isLoading = true;
        if (sendBtn) sendBtn.disabled = true;

        addMessage(message, 'user');
        showTyping();

        try {
            const body = { message: message };
            if (sessionId) body.session_id = sessionId;

            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Sunucu hatası');

            sessionId = data.session_id;
            hideTyping();
            addMessage(data.response, 'bot', data.tools_used);
        } catch (err) {
            hideTyping();
            addMessage('Hata: ' + err.message, 'bot');
        } finally {
            isLoading = false;
            updateSendButton();
        }
    }

    function updateSendButton() {
        if (sendBtn && messageInput) {
            sendBtn.disabled = isLoading || !messageInput.value.trim();
        }
    }

    function autoResize() {
        if (messageInput) {
            messageInput.style.height = 'auto';
            messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
        }
    }

    if (messageInput) {
        messageInput.addEventListener('input', () => { updateSendButton(); autoResize(); });
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey && !sendBtn.disabled) {
                e.preventDefault();
                const msg = messageInput.value.trim();
                messageInput.value = '';
                sendMessage(msg);
            }
        });
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', () => {
            const msg = messageInput.value.trim();
            messageInput.value = '';
            sendMessage(msg);
        });
    }

    document.querySelectorAll('.quick-btn, .chip').forEach(btn => {
        btn.addEventListener('click', () => {
            const msg = btn.getAttribute('data-message');
            if (msg && messageInput) {
                messageInput.value = msg;
                autoResize();
                updateSendButton();
                messageInput.focus();
                const start = msg.indexOf('['), end = msg.indexOf(']');
                if (start !== -1 && end !== -1) messageInput.setSelectionRange(start, end + 1);
            }
        });
    });

    if (clearChat) {
        clearChat.addEventListener('click', () => {
            if (chatMessages) chatMessages.innerHTML = '';
            if (welcomeContainer) welcomeContainer.style.display = 'flex';
            sessionId = null;
        });
    }

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
    }

    async function checkHealth() {
        try {
            const res = await fetch('/health');
            const data = await res.json();
            const dot = document.getElementById('status-dot');
            const text = document.getElementById('status-text');
            if (dot && text) {
                dot.style.background = data.agent_ready ? '#2ecc71' : '#e74c3c';
                text.textContent = data.agent_ready ? 'AI Agent Aktif' : 'API Key Eksik';
            }
        } catch (e) { /* ignore */ }
    }

    checkHealth();
    if (messageInput) messageInput.focus();
})();