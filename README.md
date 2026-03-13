# HSTU Library Management System

A desktop-based Library Management System built with **Python**, **Tkinter**, and **MySQL**. It supports admin and student login, book and student management, issue/return flow, and overdue fine handling.

## Features

- Admin and student login
- Secure password hashing with PBKDF2
- Book CRUD management
- Student registration with auto-generated institutional email
- Book issue and return workflow
- Automatic due-date and overdue fine calculation
- Fine payment tracking
- Student profile view
- HSTU library information and website link

## Project Structure

```text
HSTU_LMS_GithubReady/
├── gui/
├── images/
├── models/
├── utils/
├── db.py
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Tech Stack

- Python 3.10+
- Tkinter
- MySQL
- mysql-connector-python
- Pillow

## Setup

### 1) Clone the repository

```bash
git clone <your-repo-url>
cd HSTU_LMS_GithubReady
```

### 2) Create and activate a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

Copy `.env.example` to `.env` and update the values.

```bash
copy .env.example .env
```

or on Linux/macOS:

```bash
cp .env.example .env
```

Make sure MySQL is running and that the configured user has permission to create a database.

### 5) Run the project

```bash
python main.py
```

On first run, the app will:

- create the database if it does not exist
- create the required tables
- create a default admin account using the values from `.env`

## Default Admin Login

The default admin account comes from `.env`:

- Username: `LMS_DEFAULT_ADMIN_USERNAME`
- Password: `LMS_DEFAULT_ADMIN_PASSWORD`

Change these values before sharing screenshots or demo videos.

## Security Improvements Included

This GitHub-ready version removes hardcoded database credentials and stores passwords using hashed values instead of plain text. It also excludes local virtual environments, cache files, and editor settings from version control.

## Important Notes

- Issuing a book decreases available quantity.
- Returning a book increases available quantity.
- The app prevents deleting a student with active loans.
- The app prevents deleting a book that is currently issued.

## Suggested GitHub Repo Description

> Desktop-based Library Management System built with Python, Tkinter, and MySQL, featuring secure login, book issuing/return flow, student management, and overdue fine tracking.

## Suggested Topics

`python` `tkinter` `mysql` `desktop-application` `library-management-system` `crud-app`
