setTimeout(() => {
    const messages = document.querySelectorAll('.message');

    messages.forEach((msg) => {
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 400); // Remove from DOM after fade-out
    })
}, 4000);