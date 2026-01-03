const topics = [
  { id: 1, name: "Technology" },
  { id: 2, name: "Movies" },
  { id: 3, name: "Music" },
  { id: 4, name: "Sports" },
  { id: 5, name: "Travel" },
  { id: 6, name: "Books" }
];

let currentEmail = null;
let currentUser = null;
let ws = null;

function show(id) {
  document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
  document.getElementById(id).style.display = 'block';
}

async function sendCode() {
  const email = document.getElementById('email').value.trim();
  if (!email) return alert('Enter email');
  try {
    const res = await fetch('/api/v1/', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ email })
    });
    if (!res.ok) throw new Error(await res.text());
    currentEmail = email;
    document.getElementById('verify-email').innerText = email;
    show('step-verify');
  } catch (e) {
    alert('Error sending code: ' + e);
  }
}

async function verifyCode() {
  const code = document.getElementById('code').value.trim();
  if (!code.match(/^\d{6}$/)) return alert('Code must be 6 digits');
  try {
    const res = await fetch('/api/v1/verify-code', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ email: currentEmail, code })
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text);
    }
    show('step-profile');
    renderTopics();
    document.getElementById('profile-email').innerText = currentEmail;
  } catch (e) {
    alert('Invalid code or error: ' + e);
  }
}

function renderTopics() {
  const container = document.getElementById('topics');
  container.innerHTML = '';
  topics.forEach(t => {
    const btn = document.createElement('button');
    btn.className = 'topic-btn';
    btn.innerText = t.name;
    btn.onclick = () => selectTopic(t.id, t.name);
    container.appendChild(btn);
  });
}

let selectedTopicId = null;
let selectedTopicName = null;
function selectTopic(id, name) {
  selectedTopicId = id;
  selectedTopicName = name;
  document.getElementById('selected-topic').innerText = name;
}

async function createProfile() {
  const username = document.getElementById('username').value.trim();
  if (!username || username.length < 3) return alert('Username min 3 chars');
  if (!selectedTopicId) return alert('Select a topic');
  try {
    const res = await fetch('/api/v1/login', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ email: currentEmail, username })
    });
    if (!res.ok) throw new Error(await res.text());
    // token cookie should be set; now fetch /me
    const meRes = await fetch('/api/v1/me');
    if (!meRes.ok) throw new Error('Unable to get user info');
    currentUser = await meRes.json();
    document.getElementById('chat-username').innerText = currentUser.username;
    document.getElementById('chat-topic').innerText = selectedTopicName;
    show('step-chat');
    joinChat(selectedTopicId, currentUser);
  } catch (e) {
    alert('Error creating profile: ' + e);
  }
}

function joinChat(roomId, user) {
  const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${location.host}/api/v1/ws/chat/${roomId}/${user.id}?username=${encodeURIComponent(user.username)}`;
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    addSystemMessage('Connected to chat.');
  };
  ws.onmessage = (ev) => {
    try {
      const data = JSON.parse(ev.data);
      addMessage(data.text, data.is_self);
    } catch (e) {
      addSystemMessage(ev.data);
    }
  };
  ws.onclose = () => addSystemMessage('Disconnected.');
  ws.onerror = (e) => addSystemMessage('WebSocket error');
}

function sendMessage() {
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;
  if (!ws || ws.readyState !== WebSocket.OPEN) return alert('WebSocket not connected');
  ws.send(text);
  input.value = '';
}

function addMessage(text, isSelf) {
  const list = document.getElementById('messages');
  const el = document.createElement('div');
  el.className = 'message ' + (isSelf ? 'self' : 'other');
  el.innerText = text;
  list.appendChild(el);
  list.scrollTop = list.scrollHeight;
}

function addSystemMessage(text) {
  const list = document.getElementById('messages');
  const el = document.createElement('div');
  el.className = 'message system';
  el.innerText = text;
  list.appendChild(el);
  list.scrollTop = list.scrollHeight;
}

// Initialize
show('step-email');

window.sendCode = sendCode;
window.verifyCode = verifyCode;
window.createProfile = createProfile;
window.sendMessage = sendMessage;
