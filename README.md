# Warehouse Stock Tracking System

A Django-based MVP to track stock movements in a small warehouse.  
Manages products, stock transactions, and transaction details.

## Features

- Product management (add/view products)
- Stock in/out transaction tracking
- Transaction detail management
- Clean API design and basic UI

## Tech Stack

- Python 3.11+
- Django 4.x+
- SQLite (default)
- Gunicorn (for deployment)
- Render.com or PythonAnywhere for hosting

## Database Schema

- **prodmast** → `Product` model: Product details
- **stckmain** → `StockTransaction` model: Transaction header
- **stckdetail** → `StockDetail` model: Transaction line items

## Getting Started

### Local Development

1. **Clone the repo:**
    ```sh
    git clone https://github.com/diljithmon170/stock_project.git
    cd stock_project
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

4. **Run the server:**
    ```sh
    python manage.py runserver
    ```

5. **Access the app:**  
   Open [http://localhost:8000](http://localhost:8000) in your browser.

### Deployment (Render.com)

- See `render.yaml` for Render deployment configuration.
- Set environment variables as shown in the file.

## Folder Structure

```
├── inventory/         # Django app for warehouse logic
├── stock_project/     # Django project settings
├── manage.py
├── requirements.txt
├── render.yaml
└── README.md
```

## License

This project is open-source and free to
