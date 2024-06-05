document.getElementById('registerForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const nickname = document.getElementById('nickname').value;
    const phone = document.getElementById('phone').value;

    const response = await fetch('/api/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nickname, phone })
    });
    const data = await response.json();
    console.log(data);
});

document.getElementById('searchButton').addEventListener('click', async () => {
    const query = document.getElementById('searchQuery').value;

    const response = await fetch(`/api/users/?query=${query}`);
    const data = await response.json();
    document.getElementById('searchResult').innerText = JSON.stringify(data);
});

document.getElementById('messageForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const messageContent = document.getElementById('messageContent').value;

    const response = await fetch('/api/messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ conversation_id: 1, sender_id: 1, content: messageContent })
    });
    const data = await response.json();
    console.log(data);
});
