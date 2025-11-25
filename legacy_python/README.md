# The Nest 둥지

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-black.svg)

**The Nest** is a minimalist and secure personal *cloud storage* server built from scratch using Python and Flask. This project is designed to give you full control over your data, allowing you to store, manage, and access files safely through a clean and simple web interface.

---

## 📖 Table of Contents
- [Project Philosophy](#-project-philosophy)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Installation & Configuration](#-installation--configuration)
- [API Documentation](#-api-documentation)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💡 Project Philosophy
In an era where data is a commodity, **The Nest** is built on the idea of data sovereignty. Its goal is to provide a transparent and self-controlled alternative to commercial cloud services, while also serving as an excellent learning project for full-stack web application development.

---

## ✨ Key Features
- **🔐 Secure Authentication:** Token-based registration & login system (JWT) with password hashing (Bcrypt).
- **👤 Isolated Storage:** Each user has their own private storage space. Files cannot be accessed by other users.
- **⚡ Full File Operations (CRUD):** Support for **Upload**, **List**, **Download**, and **Delete**.
- **🌐 Responsive Web Interface:** Separate pages for authentication (login/register) and the main file dashboard.
- **🧩 RESTful API:** Cleanly structured backend, making it easy to integrate with future clients like mobile or desktop apps.

---

## 🛠️ Technology Stack
* **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Bcrypt, PyJWT  
* **Database:** SQLite (for development simplicity)  
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

---

## 🚀 Installation & Configuration

### Prerequisites
- Python 3.8+
- Git

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/YOUR_USERNAME/the-nest.git
    cd the-nest
    ```

2. **Create Virtual Environment & Install Dependencies**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    *(Note: You must create `requirements.txt` using `pip freeze > requirements.txt`.)*

3. **Configure the Application**
    Edit the `app.py` file and replace the `SECRET_KEY` with a long, unique, random string:
    ```python
    app.config['SECRET_KEY'] = 'replace-with-a-very-hard-to-guess-secret-key'
    ```

4. **Initialize the Database**
    ```bash
    python
    ```
    ```python
    >>> from app import app, db
    >>> with app.app_context():
    ...     db.create_all()
    ...
    >>> exit()
    ```

5. **Run the Server**
    - **Backend:**  
      ```bash
      flask run --host=0.0.0.0
      ```
    - **Frontend:**  
      ```bash
      python3 -m http.server 8000
      ```

6. **Access the Application**
   Open in browser:  
   `http://127.0.0.1:8000/register.html`

---

## 📋 API Documentation

All authenticated endpoints require a token in the header:

`x-access-token: <YOUR_JWT_TOKEN>`

| Method | Endpoint                    | Description                                  | Token Required? |
|--------|-----------------------------|-----------------------------------------------|-----------------|
| `POST` | `/api/register`             | Register a new user                           | No              |
| `POST` | `/api/login`                | Log in and receive JWT token                  | No              |
| `POST` | `/api/upload`               | Upload a new file                             | Yes             |
| `GET`  | `/api/files`                | Get list of user-owned files                  | Yes             |
| `GET`  | `/api/download/<filename>`  | Download a specific file                      | Yes             |
| `DELETE` | `/api/files/<filename>`   | Delete a specific file                        | Yes             |

---

## 🗺️ Roadmap
- [ ] **Android Client App:** Sync and auto-upload features.
- [ ] **Folder Support:** Create and manage directories.
- [ ] **UI/UX Improvements:** Add Bootstrap or Tailwind CSS.
- [ ] **File Sharing:** Secure shareable links.

---
# The Nest 둥지

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-black.svg)

**The Nest** is a minimalist and secure personal *cloud storage* server built from scratch using Python and Flask. This project is designed to give you full control over your data, allowing you to store, manage, and access files safely through a clean and simple web interface.

---

## 📖 Table of Contents
- [Project Philosophy](#-project-philosophy)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Installation & Configuration](#-installation--configuration)
- [API Documentation](#-api-documentation)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💡 Project Philosophy
In an era where data is a commodity, **The Nest** is built on the idea of data sovereignty. Its goal is to provide a transparent and self-controlled alternative to commercial cloud services, while also serving as an excellent learning project for full-stack web application development.

---

## ✨ Key Features
- **🔐 Secure Authentication:** Token-based registration & login system (JWT) with password hashing (Bcrypt).
- **👤 Isolated Storage:** Each user has their own private storage space. Files cannot be accessed by other users.
- **⚡ Full File Operations (CRUD):** Support for **Upload**, **List**, **Download**, and **Delete**.
- **🌐 Responsive Web Interface:** Separate pages for authentication (login/register) and the main file dashboard.
- **🧩 RESTful API:** Cleanly structured backend, making it easy to integrate with future clients like mobile or desktop apps.

---

## 🛠️ Technology Stack
* **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Bcrypt, PyJWT  
* **Database:** SQLite (for development simplicity)  
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

---

## 🚀 Installation & Configuration

### Prerequisites
- Python 3.8+
- Git

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/YOUR_USERNAME/the-nest.git
    cd the-nest
    ```

2. **Create Virtual Environment & Install Dependencies**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    *(Note: You must create `requirements.txt` using `pip freeze > requirements.txt`.)*

3. **Configure the Application**
    Edit the `app.py` file and replace the `SECRET_KEY` with a long, unique, random string:
    ```python
    app.config['SECRET_KEY'] = 'replace-with-a-very-hard-to-guess-secret-key'
    ```

4. **Initialize the Database**
    ```bash
    python
    ```
    ```python
    >>> from app import app, db
    >>> with app.app_context():
    ...     db.create_all()
    ...
    >>> exit()
    ```

5. **Run the Server**
    - **Backend:**  
      ```bash
      flask run --host=0.0.0.0
      ```
    - **Frontend:**  
      ```bash
      python3 -m http.server 8000
      ```

6. **Access the Application**
   Open in browser:  
   `http://127.0.0.1:8000/register.html`

---

## 📋 API Documentation

All authenticated endpoints require a token in the header:

`x-access-token: <YOUR_JWT_TOKEN>`

| Method | Endpoint                    | Description                                  | Token Required? |
|--------|-----------------------------|-----------------------------------------------|-----------------|
| `POST` | `/api/register`             | Register a new user                           | No              |
| `POST` | `/api/login`                | Log in and receive JWT token                  | No              |
| `POST` | `/api/upload`               | Upload a new file                             | Yes             |
| `GET`  | `/api/files`                | Get list of user-owned files                  | Yes             |
| `GET`  | `/api/download/<filename>`  | Download a specific file                      | Yes             |
| `DELETE` | `/api/files/<filename>`   | Delete a specific file                        | Yes             |

---

## 🗺️ Roadmap
- [ ] **Android Client App:** Sync and auto-upload features.
- [ ] **Folder Support:** Create and manage directories.
- [ ] **UI/UX Improvements:** Add Bootstrap or Tailwind CSS.
- [ ] **File Sharing:** Secure shareable links.

---

## 🙌 Contributing
Contributions, issues, and feature requests are welcome! Feel free to fork the repo and open a pull request.

---

## Android Installation (PWA)

You can install "The Nest" on your Android device as a Progressive Web App (PWA):

1.  Open Chrome on your Android device.
2.  Navigate to the server's URL (e.g., `http://<your-pc-ip>:5000`).
3.  Tap the menu button (three dots) in Chrome.
4.  Tap **"Add to Home Screen"** or **"Install App"**.
5.  The app will be installed and appear in your app drawer.

## 📜 License
This project is licensed under the **MIT License**.  
See the `LICENSE` file for more information.
