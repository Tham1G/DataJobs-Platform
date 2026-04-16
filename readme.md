<img width="1915" height="971" alt="image" src="https://github.com/user-attachments/assets/aeb9f94c-77b2-47f2-9468-6fee67b5049d" />



# DataJobs Platform – Job Market Intelligence System

DataJobs Platform is a full-stack job analytics system that enables users to explore, query, and extract insights from a dataset of over **7 million job records**. It combines a FastAPI backend, Microsoft SQL Server database, and a React frontend to deliver data-driven insights such as salary trends, in-demand skills, and job distributions.

---

## 🚀 Features

* 🔍 Search and filter job listings
* 📊 Analyze salary trends and job market patterns
* 🧠 Identify in-demand skills across industries
* ⚡ High-performance FastAPI backend
* 🗄️ SQL Server integration with large-scale dataset (7M+ records)
* 💻 Interactive React frontend (Vite)
* 🔄 RESTful API for flexible data access

---

## 🏗️ Tech Stack

**Backend**

* FastAPI (Python)
* SQLAlchemy / Pydantic
* Microsoft SQL Server

**Frontend**

* React (Vite)
* JavaScript / HTML / CSS

**Database**

* SQL Server (DataJobs dataset)

---

## 📂 Project Structure

```
DataJobs-Platform/
├── API/                  # FastAPI backend
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── database.py
│
├── frontend/             # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Tham1G/DataJobs-Platform.git
cd DataJobs-Platform
```

---

### 2. Backend Setup (FastAPI)

```bash
cd API
python -m venv venv
venv\Scripts\activate   # Windows

pip install -r ../requirements.txt
```

Create a `.env` file:

```env
DB_HOST=your_server
DB_NAME=datajobs
DB_USER=your_username
DB_PASSWORD=your_password
```

Run the backend:

```bash
uvicorn main:app --reload
```

API available at:

```
http://127.0.0.1:8000
```

---

### 3. Frontend Setup (React)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 🔌 Example API Endpoints

| Endpoint         | Description            |
| ---------------- | ---------------------- |
| `/jobs`          | Retrieve job listings  |
| `/jobs/search`   | Search jobs by keyword |
| `/skills/top`    | Top in-demand skills   |
| `/salary/trends` | Salary insights        |

---

## 📊 Use Cases

* Explore job market trends
* Identify high-paying skills
* Analyze demand for technologies (SQL, Python, Cloud, etc.)
* Build data-driven career insights tools

---

## 🤖 AI-Assisted Development

AI-assisted tools were used during development to accelerate implementation, debugging, and iteration.
All core system design, database integration, and application logic were independently implemented and validated.

---

## 🔒 Environment Variables

Sensitive configuration is stored in `.env` (excluded from version control).

Example:

```
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

---

## 🧠 Future Improvements

* 📈 Data visualizations (charts & dashboards)
* 🔐 Authentication & user accounts
* ☁️ Cloud deployment (Azure / AWS)
* ⚡ Query optimization for large datasets
* 📊 Advanced filtering and analytics

---

## 📄 License

MIT License

---

## 👤 Author

**Thami Goqo**
Application & Systems Support Technician
Aspiring Backend / Data Engineer

---

## ⭐ Final Note

This project demonstrates the ability to design and build a **full-stack data platform**, integrate large datasets, and expose meaningful insights through APIs and user interfaces.
