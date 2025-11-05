# ⚙️ IP Configuration

A cross-platform tool built with **React.js** (frontend) and **Python Flask** (backend) to manage and change the IP address configuration of a device.  
The project supports both **Linux** and **Windows** operating systems and interacts with **Hercules software** to fetch and manage network data.

---

## 🖥️ Overview

The **IP Configuration** project provides a simple and intuitive web interface to:
- View current IP settings of the device.
- Change or update the IP address.
- Fetch and display network configuration data from **Hercules software**.
- Support both Linux and Windows environments.

---

## 🛠️ Tech Stack

**Frontend:** React.js  
**Backend:** Python Flask  
**Data Source:** Hercules Software  
**OS Compatibility:** Linux & Windows  

---

## ⚡ Features

- 🔍 View current IP configuration  
- 📝 Update device IP address  
- 🌐 Cross-platform compatibility (Linux & Windows)  
- 🔄 Real-time data fetching from Hercules software  
- 🧩 REST API integration between React and Flask  

---

## 🚀 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/DevduttKumar/ip-configuration.git
cd ip-configuration
```
### 2️⃣ Backend Setup (Flask):-
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python app.py
```
### 3️⃣ Frontend Setup (React):-
```bash
cd frontend
npm install
npm run dev
