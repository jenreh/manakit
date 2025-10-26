// Scroll to bottom helper for assistant messages
(function () {
    function init() {
        var btn = document.getElementById('btn-to-bottom');
        if (!btn) {
            setTimeout(init, 100);
            return;
        }

        btn.removeEventListener('click', handleClick);
        btn.addEventListener('click', handleClick);
    }

    function handleClick() {
        // Try to find the main chat container and scroll to bottom
        var chat = document.querySelector('.chat-messages') || document.querySelector('.messages');
        if (chat) {
            chat.scrollTop = chat.scrollHeight;
        } else {
            // Fallback to window scroll
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
