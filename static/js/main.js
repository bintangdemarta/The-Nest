const API_URL = '/api';

// Helper to get token
function getToken() {
    return localStorage.getItem('token');
}

// Register
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const messageDiv = document.getElementById('message');

        try {
            const response = await fetch(`${API_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();

            if (response.ok) {
                messageDiv.innerHTML = `<span style="color: green">${data.message}</span>`;
                setTimeout(() => window.location.href = '/login.html', 1500);
            } else {
                messageDiv.innerHTML = `<span style="color: red">${data.message}</span>`;
            }
        } catch (error) {
            messageDiv.innerHTML = `<span style="color: red">An error occurred</span>`;
        }
    });
}

// Login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const messageDiv = document.getElementById('message');

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.token);
                window.location.href = '/dashboard.html';
            } else {
                messageDiv.innerHTML = `<span style="color: red">Invalid credentials</span>`;
            }
        } catch (error) {
            messageDiv.innerHTML = `<span style="color: red">An error occurred</span>`;
        }
    });
}

// Logout
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        window.location.href = '/login.html';
    });
}

// Dashboard Logic
async function loadFiles() {
    const fileList = document.getElementById('fileList');
    const token = getToken();

    try {
        const response = await fetch(`${API_URL}/files`, {
            headers: { 'x-access-token': token }
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login.html';
            return;
        }

        const data = await response.json();
        fileList.innerHTML = '';

        if (data.files.length === 0) {
            fileList.innerHTML = '<li>No files found.</li>';
            return;
        }

        data.files.forEach(file => {
            const li = document.createElement('li');
            li.innerHTML = `
                <a href="/file.html?id=${file.id}" class="download-link">${file.filename}</a>
                <span style="font-size: 0.8rem; color: #666; margin-right: 1rem;">${formatSize(file.size)}</span>
            `;
            fileList.appendChild(li);
        });
    } catch (error) {
        console.error('Error loading files:', error);
    }
}

function formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function loadFileDetails(fileId) {
    const detailsDiv = document.getElementById('fileDetails');
    const token = getToken();

    try {
        const response = await fetch(`${API_URL}/files/${fileId}`, {
            headers: { 'x-access-token': token }
        });

        if (response.ok) {
            const file = await response.json();
            detailsDiv.innerHTML = `
                <h3>${file.filename}</h3>
                <p><strong>Size:</strong> ${formatSize(file.size)}</p>
                <p><strong>Uploaded:</strong> ${new Date(file.upload_date).toLocaleString()}</p>
                <div style="margin-top: 2rem;">
                    <a href="${API_URL}/download/${file.filename}" class="btn" target="_blank">Download</a>
                    <button class="delete-btn btn" onclick="deleteFile('${file.filename}', true)">Delete</button>
                </div>
            `;
        } else {
            detailsDiv.innerHTML = '<p>File not found.</p>';
        }
    } catch (error) {
        detailsDiv.innerHTML = '<p>Error loading details.</p>';
    }
}

async function deleteFile(filename, redirect = false) {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) return;

    const token = getToken();
    try {
        const response = await fetch(`${API_URL}/files/${filename}`, {
            method: 'DELETE',
            headers: { 'x-access-token': token }
        });

        if (response.ok) {
            if (redirect) {
                window.location.href = '/dashboard.html';
            } else {
                loadFiles();
            }
        } else {
            alert('Failed to delete file');
        }
    } catch (error) {
        alert('Error deleting file');
    }
}
window.deleteFile = deleteFile;

// Upload
const uploadForm = document.getElementById('uploadForm');
if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        const token = getToken();
        const messageDiv = document.getElementById('message');
        messageDiv.innerHTML = 'Uploading...';

        try {
            const response = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                headers: { 'x-access-token': token },
                body: formData
            });

            const data = await response.json();
            if (response.ok) {
                messageDiv.innerHTML = `<span style="color: green">${data.message}</span>`;
                fileInput.value = '';
                loadFiles();
            } else {
                messageDiv.innerHTML = `<span style="color: red">${data.message}</span>`;
            }
        } catch (error) {
            messageDiv.innerHTML = `<span style="color: red">Upload failed</span>`;
        }
    });
}
