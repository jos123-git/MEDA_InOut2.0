# InOut
Capstone Project


🚀 INOUT HR Portal - Setup Guide
This is the official HR Monitoring Web Portal. Follow these steps to set up the environment on your local machine.

📋 Prerequisites
Ensure you have the following installed:

Python 3.10+

PostgreSQL (Ensure the service is running)

VS Code Extensions: Python and Live Server

🗄️ 1. Database Setup
You need to create the database and import the sample data provided in the project.

Create the Database: Open your terminal and run:

Bash

psql -U postgres -c "CREATE DATABASE inout_db;"
Import Sample Data: Navigate to the folder containing inout_db_backup.sql and run:

Bash

psql -U postgres -d inout_db -f inout_db_backup.sql
Check Credentials: Open backend/database.py. If your Postgres password is not postgres, update the SQLALCHEMY_DATABASE_URL line with your actual password.

⚙️ 2. Backend Setup (FastAPI)
Open your terminal in the backend folder.

Install dependencies:

Bash

pip install fastapi uvicorn sqlalchemy psycopg2-binary
Start the server:

Bash

uvicorn main:app --reload
The backend is live when you see Uvicorn running on http://127.0.0.1:8000.

💻 3. Frontend Setup (Web Interface)
Open frontend/scripts/app.js.

Ensure the API URL is set to local:

JavaScript

const API_BASE_URL = "http://127.0.0.1:8000";
Open frontend/index.html in VS Code.

Right-click the file and select "Open with Live Server".

🛠️ Troubleshooting
"ModuleNotFoundError": Ensure you cd backend before running the uvicorn command.

"Connection Refused": Check if your PostgreSQL service is actually started.

Empty Table: If the "Staff List" is empty, make sure the psql import command in Step 1 finished without errors.
