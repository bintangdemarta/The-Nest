# The Nest 둥지

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-black.svg)

**The Nest** adalah server *cloud storage* pribadi yang minimalis dan aman, dibangun dari nol menggunakan Python dan Flask. Proyek ini dirancang untuk memberikan kontrol penuh atas data Anda, memungkinkan Anda untuk menyimpan, mengelola, dan mengakses file dengan aman dari antarmuka web yang bersih.

---
## 📖 Daftar Isi
- [Filosofi Proyek](#-filosofi-proyek)
- [Fitur Utama](#-fitur-utama)
- [Tumpukan Teknologi](#-tumpukan-teknologi)
- [Instalasi & Konfigurasi](#-instalasi--konfigurasi)
- [Dokumentasi API](#-dokumentasi-api)
- [Roadmap](#-roadmap)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

---
## 💡 Filosofi Proyek
Di era di mana data adalah komoditas, "The Nest" dibangun di atas gagasan kedaulatan data. Tujuannya adalah untuk menyediakan alternatif yang transparan dan dapat dikontrol sendiri dibandingkan layanan cloud komersial, sekaligus menjadi proyek pembelajaran yang sangat baik untuk pengembangan aplikasi web full-stack.

---
## ✨ Fitur Utama
- **🔐 Otentikasi Aman:** Sistem registrasi & login berbasis token (JWT) dengan hashing password (Bcrypt).
- **👤 Penyimpanan Terisolasi:** Setiap pengguna memiliki ruang penyimpanan pribadi. File tidak dapat diakses oleh pengguna lain.
- **⚡ Operasi File Lengkap (CRUD):** Fungsionalitas untuk **Upload**, **List** (melihat daftar), **Download**, dan **Delete** file.
- **🌐 Antarmuka Web Responsif:** Halaman terpisah untuk otentikasi (login/registrasi) dan dasbor file utama.
- **🧩 API RESTful:** Backend terstruktur yang jelas, memudahkan integrasi dengan klien lain di masa depan (misalnya, aplikasi mobile atau desktop).

---
## 🛠️ Tumpukan Teknologi
* **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Bcrypt, PyJWT
* **Database:** SQLite (untuk kemudahan pengembangan)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

---
## 🚀 Instalasi & Konfigurasi

### Prasyarat
- Python 3.8+
- Git

### Langkah-langkah
1.  **Clone Repositori:**
    ```bash
    git clone [https://github.com/NAMA_USER_ANDA/the-nest.git](https://github.com/NAMA_USER_ANDA/the-nest.git)
    cd the-nest
    ```

2.  **Buat Lingkungan Virtual & Instal Dependensi:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
    *(Catatan: Anda perlu membuat file `requirements.txt` terlebih dahulu dengan `pip freeze > requirements.txt`)*

3.  **Konfigurasi Aplikasi:**
    Di dalam file `app.py`, pastikan Anda mengubah `SECRET_KEY` menjadi string acak yang panjang dan unik.
    ```python
    app.config['SECRET_KEY'] = 'ganti-dengan-kunci-rahasia-yang-sangat-sulit-ditebak'
    ```

4.  **Inisialisasi Database:**
    Jalankan perintah ini satu kali untuk membuat file `database.db`.
    ```bash
    # Buka Python shell
    python
    ```
    ```python
    >>> from app import app, db
    >>> with app.app_context():
    ...     db.create_all()
    ...
    >>> exit()
    ```

5.  **Jalankan Server:**
    * **Terminal 1 (Backend):** `flask run --host=0.0.0.0`
    * **Terminal 2 (Frontend):** `python3 -m http.server 8000`

6.  **Akses Aplikasi:** Buka browser dan kunjungi `http://127.0.0.1:8000/register.html`.

---
## 📋 Dokumentasi API

Semua *endpoint* yang memerlukan otentikasi harus menyertakan token di header: `x-access-token: <TOKEN_JWT_ANDA>`.

| Method | Endpoint                    | Deskripsi                               | Memerlukan Token? |
| :----- | :-------------------------- | :-------------------------------------- | :---------------: |
| `POST` | `/api/register`             | Mendaftarkan pengguna baru.             |        Tidak      |
| `POST` | `/api/login`                | Login dan mendapatkan token JWT.        |        Tidak      |
| `POST` | `/api/upload`               | Mengunggah file baru.                   |         Ya        |
| `GET`  | `/api/files`                | Mendapatkan daftar file milik pengguna. |         Ya        |
| `GET`  | `/api/download/<filename>`  | Mengunduh file tertentu.                |         Ya        |
| `DELETE`| `/api/files/<filename>`   | Menghapus file tertentu.                |         Ya        |

---
## 🗺️ Roadmap
-   [ ] **Aplikasi Klien Android:** Membangun aplikasi native untuk sinkronisasi dan unggah otomatis.
-   [ ] **Dukungan Folder:** Kemampuan untuk membuat dan mengelola direktori.
-   [ ] **Peningkatan UI/UX:** Mengintegrasikan framework CSS seperti Bootstrap atau Tailwind CSS.
-   [ ] **Berbagi File:** Membuat tautan berbagi yang aman untuk file.

---
## 🙌 Kontribusi
Kontribusi, isu, dan permintaan fitur sangat diterima! Jangan ragu untuk membuat *fork* repositori ini dan membuka *pull request*.

---
## 📜 Lisensi
Proyek ini dilisensikan di bawah **MIT License**. Lihat file `LICENSE` untuk detail lebih lanjut.
