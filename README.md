# Staboost - Social Media Marketing Platform

Staboost is a full-stack social media marketing platform designed to integrate with the CloutFlash API. It provides a comprehensive solution for users to purchase social media engagement services, manage their orders, and track their progress. The platform includes a secure payment system, a user-friendly interface, and a powerful admin panel for platform management.

## Key Features (Version 1.0)

*   **User Authentication:** Secure user registration and login system with JWT-based authentication.
*   **CloutFlash Integration:** Seamless integration with the CloutFlash API to fetch a wide range of social media services.
*   **Dynamic Pricing:** A flexible pricing model that applies a customizable markup percentage to the original API prices.
*   **Wallet System:** Each user has a personal wallet to store credits, which can be used to purchase services.
*   **Order Management:** Users can place orders for services, and the system automatically handles the order with the CloutFlash API.
*   **Background Order Tracking:** A robust background task system using Celery and Redis to automatically track and update the status of orders in real-time.
*   **Paystack Payment Gateway:** A secure payment system powered by Paystack, allowing users to easily fund their wallets.
*   **Modern Frontend:** A responsive and modern frontend built with React, Vite, and Tailwind CSS.

## Technology Stack

### Backend
*   **Framework:** Django, Django REST Framework
*   **Database:** PostgreSQL (production), SQLite (development)
*   **Asynchronous Tasks:** Celery, Redis
*   **API Testing:** N/A (but recommended: Pytest)
*   **Web Server:** Gunicorn

### Frontend
*   **Framework:** React
*   **Build Tool:** Vite
*   **Styling:** Tailwind CSS
*   **Routing:** React Router

## Local Development Setup

### Prerequisites
*   Python 3.10+
*   Node.js 18+ and npm
*   PostgreSQL
*   Redis

### Backend Setup
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Navigate to the backend directory:**
    ```bash
    cd staboost
    ```

3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up environment variables:**
    Create a `.env` file in the `staboost` directory and add the necessary variables (see Configuration section).

6.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The backend will be available at `http://localhost:8000`.

### Frontend Setup
1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

## Configuration

The following environment variables are required to run the application. Create a `.env` file in the `staboost` directory for local development or set them directly in your deployment environment.

*   `SECRET_KEY`: A secret key for a particular Django installation.
*   `DEBUG`: Set to `True` for development, `False` for production.
*   `ALLOWED_HOSTS`: A comma-separated list of allowed hostnames (e.g., `localhost,yourdomain.com`).
*   `DATABASE_URL`: The URL for your PostgreSQL database (e.g., `postgres://user:password@host:port/dbname`).
*   `CELERY_BROKER_URL`: The URL for your Redis instance (e.g., `redis://localhost:6379/0`).
*   `CELERY_RESULT_BACKEND`: Same as `CELERY_BROKER_URL`.
*   `CLOUTFLASH_API_URL`: The URL for the CloutFlash API (e.g., `https://app.cloutflash.com/api/v2`).
*   `CLOUTFLASH_API_KEY`: Your API key for the CloutFlash API.
*   `DEFAULT_MARKUP_PERCENTAGE`: The default markup percentage for services (e.g., `20.0`).
*   `PAYSTACK_SECRET_KEY`: Your Paystack secret key.
*   `PAYSTACK_PUBLIC_KEY`: Your Paystack public key.

## Deployment on Render

This project is configured for easy deployment on Render using Docker.

1.  **Push your code** to a GitHub repository.
2.  **Create a new "Web Service" on Render** and connect it to your GitHub repository.
3.  **Choose Docker** as the runtime environment.
4.  **Configure the build and start commands:**
    *   **Build Command:** `./build.sh`
    *   **Start Command:** `gunicorn staboost.wsgi:application --bind 0.0.0.0:$PORT`
5.  **Set up a PostgreSQL database and a Redis instance** on Render.
6.  **Add the environment variables** listed in the Configuration section to your Render service. Make sure to use the connection URLs provided by Render for your database and Redis instance.

Render will automatically build the Docker image and deploy your application. The `build.sh` script will handle database migrations.
