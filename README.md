EasyQueue Backend
Backend API for the EasyQueue DMV wait-time prediction and queue management system.

Tech Stack
Python 3.13+
FastAPI
SQLAlchemy
MySQL
PyMySQL
Uvicorn
Setup

1. Create a Virtual Environment
python -m venv venv
Activate:
Windows PowerShell:
.\venv\Scripts\Activate.ps1

2. Install Dependencies
pip install -r requirements.txt

3. Create MySQL Database
Open MySQL Workbench and run:
CREATE DATABASE easyqueue;

4. Create .env File
Create a file named .env in the backend directory.

Example:
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/easyqueue
If your password contains special characters such as @, URL encode them.

Example:
DATABASE_URL=mysql+pymysql://root:MyPassword%40@localhost:3306/easyqueue

5. Initialize Database Tables
Run:
python -m app.db.init_db
This creates the database tables automatically.

Running the Application
Start the FastAPI server:

uvicorn app.main:app --reload
API available at:

http://127.0.0.1:8000
Swagger documentation:

http://127.0.0.1:8000/docs
Current Project Structure
backend/
│
├── app/
│   ├── api/
│   ├── constants/
│   ├── db/
│   ├── models/
│   ├── prediction_engine/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   └── main.py
│
├── tests/
├── requirements.txt
└── README.md
Current Database Models
Customer
ServiceType
QueueEntry
StaffAction

Team Notes
Do not commit .env
Do not commit venv
Pull from main before beginning work
Create feature branches for major changes when possible
