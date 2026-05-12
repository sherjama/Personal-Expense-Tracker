# 💰 Personal Expense Tracker (Flask + MySQL)

## 📌 Overview

This is a full-stack web application built using **Python Flask and MySQL** to track personal income and expenses. It provides authentication, transaction management, analytics, and PDF report generation.

---

## 🚀 Features

* User Registration & Login System
* Add / Edit / Delete Transactions
* Income & Expense Tracking
* Category-wise Expense Management
* Dashboard with Summary (Income, Expense, Balance)
* Analytics with Pie Chart Visualization
* Search Transactions by Category
* PDF Report Download
* Responsive UI using Bootstrap

---

## 🛠️ Tech Stack

* Python (Flask)
* MySQL Database
* Flask-SQLAlchemy
* Flask-Login
* HTML, CSS, Bootstrap
* Matplotlib (Graphs)
* ReportLab (PDF Generation)

---

## 📁 Project Structure

```
expense_tracker/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
│
├── templates/
├── static/
│   ├── style.css
│   └── charts/
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   (Windows)
source venv/bin/activate (Mac/Linux)
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Setup Database

Create MySQL database:

```
CREATE DATABASE expense_tracker;
```

### 5. Run Application

```
python app.py
```

### 6. Open Browser

```
http://127.0.0.1:5000
```

---

## 📊 Future Improvements

* Budget limit alerts
* Dark mode UI
* Mobile app version
* Email notifications
* Advanced analytics dashboard

---

## 👨‍💻 Author

Developed by: **Sherjama**
Project Type: College Final Year Project
