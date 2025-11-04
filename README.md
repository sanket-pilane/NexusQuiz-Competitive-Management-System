# 🚀 Django Quiz Platform

Welcome to the Django Quiz Platform! This is a robust and interactive web application built with Python and the Django framework. It allows administrators to create, manage, and review quizzes, while users can take them and view their results in real-time.

![Quiz App Screenshot](https://i.imgur.com/your-screenshot.png) <!-- Replace with a real screenshot URL -->

## ✨ Features

-   **👨‍🏫 Admin Dashboard**: A dedicated dashboard for administrators to manage quizzes, view attempt statistics, and add or edit questions.
-   **📝 Dynamic Quiz Creation**: Easily create quizzes with titles, descriptions, and durations. Add multiple-choice questions with a designated correct answer.
-   **⏱️ Real-Time Quiz Timer**: When taking a quiz, a countdown timer is displayed. The quiz is automatically submitted when the time runs out.
-   **📊 Instant Results**: Users receive immediate feedback on their performance, including their score and the percentage of correct answers.
-   **🔐 User Authentication**: Secure registration and login system for both regular users and administrators.
-   **🎨 Sleek Dark Theme**: A modern, eye-pleasing dark theme that is consistent across the entire application.
-   **💻 Responsive Design**: Built with Bootstrap to ensure a great experience on both desktop and mobile devices.

## 🛠️ Tech Stack

-   **Backend**: 🐍 Python, 🕸️ Django
-   **Frontend**: 📄 HTML, 🎨 CSS, 💻 JavaScript
-   **Styling**: ✨ Bootstrap 5
-   **Environment**: ❄️ Nix for reproducible development environments

## ⚙️ Setup and Installation

This project uses a Nix shell to ensure a consistent and reproducible development environment.

### Prerequisites

-   Ensure you have [Nix](https://nixos.org/download.html) installed on your system.
-   Git for cloning the repository.

### Step-by-Step Instructions

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd <project-directory>
    ```

2.  **Activate the Nix Shell**
    This command reads the `dev.nix` file and sets up an environment with the correct Python version and other necessary tools.
    ```bash
    nix-shell
    ```
    *This might take a few moments on the first run as Nix downloads the specified dependencies.*

3.  **Activate the Virtual Environment**
    The Nix environment is configured to automatically create a Python virtual environment at `.venv/`. Activate it to use the project's dependencies.
    ```bash
    source .venv/bin/activate
    ```

4.  **Install Python Dependencies**
    Install all the required Django and Python packages from the `requirements.txt` file.
    ```bash
    pip install -r mysite/requirements.txt
    ```

5.  **Apply Database Migrations**
    Set up your initial database schema by running the Django migrations.
    ```bash
    python mysite/manage.py migrate
    ```

6.  **Create a Superuser (Admin Account)**
    To access the admin dashboard and create quizzes, you need an administrator account.
    ```bash
    python mysite/manage.py createsuperuser
    ```
    Follow the prompts to set your username, email, and password.

## ▶️ Running the Application

1.  **Ensure the virtual environment is activated**:
    ```bash
    source .venv/bin/activate
    ```

2.  **Start the Development Server**:
    Use the provided shell script to run the Django development server.
    ```bash
    ./devserver.sh
    ```

3.  **Access the Application**:
    Open your web browser and navigate to `http://127.0.0.1:8000`.
    -   Log in with your superuser credentials to access the **Admin Dashboard**.
    -   Create a regular user account via the **Sign Up** page to experience the quiz-taking flow.

---

Thank you for checking out the project! Feel free to contribute or report issues. Happy coding! 🎉
