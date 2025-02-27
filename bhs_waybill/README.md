# BHS Waybill SPA

A simple Single Page Application (SPA) built with Flask, HTML5, and Bootstrap 5.

## Project Structure

```
bhs_waybill/
├── app.py                  # Flask application
├── production.py           # Production server using waitress
├── requirements.txt        # Python dependencies
├── start_production.bat    # Batch file to start in production mode
├── .env                    # Environment variables (not in version control)
├── .env.example            # Example environment variables
├── deploy/                 # Deployment configurations
│   ├── nginx.conf          # Nginx configuration template for reverse proxy
│   ├── gunicorn.service    # Systemd service file template for Gunicorn
│   ├── uwsgi.ini           # uWSGI configuration template
│   ├── uwsgi.service       # Systemd service file template for uWSGI
│   ├── supervisor.conf     # Supervisor configuration template
│   ├── generate_configs.py # Script to generate configs from templates
│   └── LINUX_DEPLOYMENT.md # Linux deployment guide
├── static/                 # Static files
│   ├── css/
│   │   └── style.css       # Custom CSS
│   └── js/
│       └── main.js         # SPA functionality
└── templates/
    └── index.html          # Main HTML template
```

## Setup and Installation

1. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```
   # Copy the example .env file
   copy .env.example .env
   
   # Edit the .env file with your settings
   ```

## Running the Application

### Development Mode

Run the application in development mode:
```
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5500/
```

### Production Mode

#### Windows

To run the application in production mode with Waitress on port 5500:

1. Run using the provided batch file:
   ```
   start_production.bat
   ```

   Or run directly:
   ```
   python production.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5500/
   ```

#### Linux

For deploying in a Linux production environment with Nginx as a reverse proxy:

1. See the detailed deployment guide in [deploy/LINUX_DEPLOYMENT.md](deploy/LINUX_DEPLOYMENT.md)

## Environment Variables

The application uses environment variables for configuration. These are stored in a `.env` file. Key variables include:

- `PORT`: The port on which the application will run (default: 5500)
- `HOST`: The host to bind to (default: 0.0.0.0)
- `FLASK_ENV`: The Flask environment (development, production)
- `DEBUG`: Whether to enable debug mode
- `DOMAIN_NAME`: Your domain name (for production)
- `NGINX_PORT`: The port Nginx will listen on (for production)
- `SSL_ENABLED`: Whether to enable SSL (for production)

See `.env.example` for a complete list of available variables.

## Features

- Single Page Application (SPA) architecture
- Responsive design with Bootstrap 5
- Navigation between different "pages" without page reload
- Contact form with client-side validation
- Interactive UI elements
- Environment-based configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details.
