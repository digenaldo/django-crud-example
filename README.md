# Django CRUD Example

This is a straightforward CRUD (Create, Read, Update, Delete) application built with Django, Bootstrap, and SQLite/PostgreSQL. It includes user authentication, product management, and a modern, professional UI.

## Features

- ✅ User authentication (Login/Register/Logout)
- ✅ Product CRUD operations (Create, Read, Update, Delete)
- ✅ Modern, responsive UI with Bootstrap
- ✅ Professional card-based design
- ✅ Form validation and error handling
- ✅ Health check endpoint for monitoring

## 🌐 Live Application

The application is hosted on **Render** and is available at:

**🔗 [https://django-crud-example-vrkp.onrender.com/](https://django-crud-example-vrkp.onrender.com/)**

### Accessing the Application

1. **Register a new account** or **login** with existing credentials
2. Once logged in, you can:
   - View all products
   - Create new products
   - Edit existing products
   - Delete products
   - View product details

### Limitations

⚠️ **Important Notes about the Hosted Version:**

- **Free Tier Limitations**: The application is hosted on Render's free tier, which has the following limitations:
  - **Spin-down after inactivity**: Free instances spin down after 15 minutes of inactivity. The first request after spin-down may take 30-60 seconds to respond while the instance starts up.
  - **No persistent storage**: Data may be reset if the database is recreated or if the service is redeployed.
  - **Limited resources**: 512 MB RAM and 0.1 CPU, which may affect performance under heavy load.
  - **No SSH access**: Direct server access is not available on the free tier.

- **Database**: The application uses SQLite in the hosted version, which is suitable for development and small-scale use but may have limitations for production workloads.

- **Performance**: Due to the free tier limitations, response times may vary, especially after periods of inactivity.

Despite these limitations, the application is fully functional and demonstrates all CRUD operations with a modern, professional interface.

## Getting Started

Follow these steps to get the project up and running on your local environment:

### Prerequisites

Make sure you have Python and PostgreSQL installed on your system.

### Installation

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/yourusername/django-crud-example.git
    ```

2. Change to the project directory:

    ```
    cd django-crud-example
    ```

3. Install the project dependencies using pip:

    ```
    pip install -r requirements.txt
    ```

4. Create the PostgreSQL database by running migrations:

    ```
    python manage.py migrate
    ```

5. Start the development server:

    ```
    python manage.py runserver
    ```

### Creating a Superuser

To access the Django admin panel, you'll need to create a superuser account:

```
python manage.py createsuperuser
```

Follow the prompts to set up your admin account, and then you can access the admin panel at `/admin`.

## Usage

### Local Development

1. Start the development server:
   ```
   python manage.py runserver
   ```

2. Access the application at `http://127.0.0.1:8000/`

3. Register a new account or login to start managing products

### Application Features

- **Product Management**: Full CRUD operations for products
- **User Authentication**: Secure login and registration system
- **Modern UI**: Professional, responsive design with Bootstrap
- **Form Validation**: Client and server-side validation
- **Error Handling**: User-friendly error messages

You can use this CRUD application as a foundation for building your own web applications. It provides basic Create, Read, Update, and Delete functionality that can be extended and customized to suit your specific needs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Deployment

This application is configured for deployment on Render. The deployment configuration includes:

- `render.yaml` - Render service configuration
- `Procfile` - Gunicorn server configuration
- WhiteNoise for static file serving
- Environment variable configuration for production settings

### Deploying to Render

1. Connect your GitHub repository to Render
2. Configure environment variables:
   - `SECRET_KEY` - Django secret key
   - `DEBUG` - Set to `False` for production
   - `ALLOWED_HOSTS` - Your Render domain
3. Render will automatically build and deploy on every push to the main branch

## Technology Stack

- **Django** - Web framework
- **Bootstrap** - Front-end framework
- **SQLite/PostgreSQL** - Database
- **Gunicorn** - WSGI HTTP Server
- **WhiteNoise** - Static file serving
- **Font Awesome** - Icons

## Acknowledgments

- Django - The web framework used
- Bootstrap - The front-end framework used
- Render - Hosting platform
- Font Awesome - Icon library

Feel free to customize and expand upon this project to create your own Django-based web applications. If you have any questions or run into any issues, please refer to the project's [GitHub Issues](https://github.com/digenaldo/django-crud-example/issues) for assistance.
