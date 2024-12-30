# SOE Project Hub

SOE Project Hub is a Django-based web application designed to streamline the process of project management, evaluation, and collaboration in academic settings. It provides tools for students to submit projects, faculty to evaluate and manage submissions, and an overall platform to foster collaboration and learning.

## Features

### General
- User authentication and role-based access for students and faculty.
- Dynamic dashboards tailored for students and faculty.
- File uploads for various project documents (e.g., abstracts, SRS, designs).
- Deadlines and evaluation tracking.
- Plagiarism checking for uploaded documents.

### Student Features
- Team management: Create or join teams.
- Dashboard to track project submissions and evaluations.
- Query submission to faculty.

### Faculty Features
- Manage project teams and evaluate submissions.
- Make announcements to guide students.
- Respond to student queries and provide feedback.

### Support and Feedback
- Students can submit support tickets or feedback.
- Faculty can reply to queries and review feedback.

## Technologies Used

- **Backend**: Django 5.0
- **Frontend**: HTML, CSS, JavaScript (with libraries like Bootstrap, jQuery)
- **Database**: SQLite
- **Additional Libraries**:
  - `PyPDF2`: For PDF text extraction.
  - `requests`: For API calls.
  - `django-widget-tweaks`: For form customization.

## Installation

### Prerequisites
- Python 3.9+
- Virtual environment tool (e.g., `venv` or `virtualenv`)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/aswinpradeepc/SOE-Project-Hub.git
   cd SOE-Project-Hub
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`.

## Usage

### Initial Setup
- Log in as the superuser to configure initial settings and roles.
- Add faculty and student users through the admin panel.

### For Students
- Register or log in to access the dashboard.
- Create or join a team.
- Upload project documents and track progress.

### For Faculty
- Log in to access the faculty dashboard.
- Manage teams, evaluate submissions, and respond to student queries.
- Use the plagiarism checker for submissions.

## Folder Structure

```
SOE-Project-Hub/
├── auth_login/       # User authentication and role management
├── project/          # Core project submission and evaluation features
├── feedback/         # Feedback and query handling
├── support/          # Support ticket management
├── templates/        # HTML templates
├── static/           # Static assets (CSS, JS, images)
├── config/           # Django project settings and URLs
├── db.sqlite3        # SQLite database
└── manage.py         # Django entry point
```
