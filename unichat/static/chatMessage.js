// ── CHAT.JS ──────────────────────────────────────────────

let currentCourse = null;
let pollInterval = null;

// ── CSRF helper ──
function getCookie(name) {
    return document.cookie.split(';')
        .find(c => c.trim().startsWith(name + '='))
        ?.split('=')[1];
}

// ── Fetch and render messages ──
function loadMessages() {
    if (!currentCourse) return;

    fetch(`/api/messages/${currentCourse}/`)
        .then(res => res.json())
        .then(data => {
            const box = document.querySelector('.messages');
            if (!box) return;

            box.innerHTML = data.length === 0
                ? '<p class="no-messages">No messages yet. Say something!</p>'
                : data.map(m => `
                    <div class="message ${m.is_me ? 'me' : 'other'}">
                        <strong>${m.author}</strong>
                        <p>${m.body}</p>
                        <span class="msg-time">${m.created_at}</span>
                    </div>
                `).join('');

            // scroll to latest message
            box.scrollTop = box.scrollHeight;
        })
        .catch(err => console.error('Failed to load messages:', err));
}

// ── Start polling every 3 seconds ──
function startPolling() {
    if (pollInterval) clearInterval(pollInterval);
    loadMessages();
    pollInterval = setInterval(loadMessages, 3000);
}

// ── Switch course on sidebar click ──
function initCourseSwitching() {
    document.querySelectorAll('.class-item').forEach(item => {
        item.addEventListener('click', () => {
            // update active state
            document.querySelectorAll('.class-item')
                .forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            // update header
            const header = document.querySelector('.chat-header');
            if (header) header.textContent = item.textContent.trim();

            // set course and reload
            currentCourse = item.dataset.courseId;
            startPolling();
        });
    });
}

// ── Send message ──
function initSendMessage() {
    const btn = document.querySelector('.chat-input button');
    const input = document.querySelector('.chat-input input');

    if (!btn || !input) return;

    function sendMessage() {
        const body = input.value.trim();
        if (!body || !currentCourse) return;

        fetch(`/api/messages/${currentCourse}/send/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ body })
        })
        .then(res => res.json())
        .then(() => {
            input.value = '';
            loadMessages();
        })
        .catch(err => console.error('Failed to send message:', err));
    }

    // send on button click
    btn.addEventListener('click', sendMessage);

    // send on Enter key
    input.addEventListener('keydown', e => {
        if (e.key === 'Enter') sendMessage();
    });
}

// ── Auto-select first course on load ──
function selectFirstCourse() {
    const first = document.querySelector('.class-item');
    if (first) {
        first.classList.add('active');
        currentCourse = first.dataset.courseId;
        const header = document.querySelector('.chat-header');
        if (header) header.textContent = first.textContent.trim();
        startPolling();
    }
}

// ── Init everything on DOM ready ──
document.addEventListener('DOMContentLoaded', () => {
    initCourseSwitching();
    initSendMessage();
    selectFirstCourse();
});