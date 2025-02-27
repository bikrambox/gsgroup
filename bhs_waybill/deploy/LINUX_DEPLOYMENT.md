# Linux Production Deployment Guide

This guide explains how to deploy the BHS Waybill Flask application in a Linux production environment using Nginx as a reverse proxy and either Gunicorn or uWSGI as the WSGI server.

## Prerequisites

- A Linux server (Ubuntu/Debian recommended)
- Python 3.8+ installed
- Nginx installed
- Domain name (optional, but recommended)

## 1. Server Setup

### Update System Packages

```bash
sudo apt update
sudo apt upgrade -y
```

### Install Required Packages

```bash
sudo apt install -y python3-pip python3-venv nginx
```

## 2. Application Setup

### Create Application Directory

```bash
# Create a directory for the application (adjust path as needed)
sudo mkdir -p /var/www/bhs_waybill
```

### Clone or Copy Application Files

```bash
# If using Git
sudo git clone https://your-repository-url.git /var/www/bhs_waybill

# Or copy files from your local machine
# scp -r /path/to/local/bhs_waybill/* user@server:/var/www/bhs_waybill/
```

### Set Permissions

```bash
sudo chown -R www-data:www-data /var/www/bhs_waybill
```

### Create Virtual Environment and Install Dependencies

```bash
cd /var/www/bhs_waybill
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
```

### Update requirements.txt for Production

Make sure your requirements.txt includes either Gunicorn or uWSGI:

```bash
# For Gunicorn
sudo venv/bin/pip install gunicorn

# For uWSGI
sudo venv/bin/pip install uwsgi
```

### Create Log Directory

```bash
sudo mkdir -p /var/log/bhs_waybill
sudo chown -R www-data:www-data /var/log/bhs_waybill
```

## 3. Environment Configuration

The application uses environment variables for configuration. These are stored in a `.env` file.

### Create and Configure the .env File

```bash
# Copy the sample .env file
sudo cp /var/www/bhs_waybill/.env.example /var/www/bhs_waybill/.env

# Edit the .env file to match your environment
sudo nano /var/www/bhs_waybill/.env
```

Update the following variables in the `.env` file:

- `PORT`: The port on which the application will run (default: 5500)
- `HOST`: The host to bind to (default: 0.0.0.0)
- `DOMAIN_NAME`: Your domain name (e.g., yourdomain.com)
- `NGINX_PORT`: The port Nginx will listen on (default: 80)
- `APP_PATH`: The absolute path to your application (e.g., /var/www/bhs_waybill)
- `VENV_PATH`: The absolute path to your virtual environment (e.g., /var/www/bhs_waybill/venv)
- `LOG_DIR`: The directory for log files (e.g., /var/log/bhs_waybill)
- `WORKERS`: Number of worker processes (default: 4)
- `THREADS`: Number of threads per worker (default: 2)
- `TIMEOUT`: Worker timeout in seconds (default: 30)
- `MAX_REQUESTS`: Maximum number of requests before worker restart (default: 5000)
- `SSL_ENABLED`: Whether to enable SSL (default: False)
- `SSL_CERT_PATH`: Path to SSL certificate (if SSL is enabled)
- `SSL_KEY_PATH`: Path to SSL key (if SSL is enabled)

### Generate Configuration Files

The application includes a script to generate configuration files from templates using environment variables:

```bash
# Make the script executable
sudo chmod +x /var/www/bhs_waybill/deploy/generate_configs.py

# Run the script to generate configuration files
sudo /var/www/bhs_waybill/venv/bin/python /var/www/bhs_waybill/deploy/generate_configs.py
```

This will generate:
- Nginx configuration file
- uWSGI or Gunicorn systemd service file
- uWSGI configuration file (if using uWSGI)
- Supervisor configuration file (if using Supervisor)

## 4. WSGI Server Configuration

You can choose either Gunicorn or uWSGI as your WSGI server. Both configurations are provided.

### Option 1: Gunicorn Setup

The systemd service file has been generated in the previous step. Now enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable bhs_waybill
sudo systemctl start bhs_waybill
```

### Option 2: uWSGI Setup

The systemd service file and uWSGI configuration have been generated in the previous step. Now enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable bhs_waybill
sudo systemctl start bhs_waybill
```

## 5. Nginx Configuration

The Nginx configuration file has been generated in the previous step. Now enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/bhs_waybill /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

## 6. SSL Configuration (Optional but Recommended)

If you've set `SSL_ENABLED=True` in your `.env` file, you'll need to obtain SSL certificates:

### Install Certbot for Let's Encrypt SSL

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### Obtain SSL Certificate

```bash
sudo certbot --nginx -d ${DOMAIN_NAME} -d www.${DOMAIN_NAME}
```

Follow the prompts to complete the SSL setup.

After obtaining the certificates, update your `.env` file with the correct paths:

```bash
SSL_CERT_PATH=/etc/letsencrypt/live/${DOMAIN_NAME}/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/${DOMAIN_NAME}/privkey.pem
```

Then regenerate the configuration files:

```bash
sudo /var/www/bhs_waybill/venv/bin/python /var/www/bhs_waybill/deploy/generate_configs.py
```

## 7. Firewall Configuration

If you're using UFW (Uncomplicated Firewall):

```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 8. Monitoring and Maintenance

### Check Service Status

```bash
sudo systemctl status bhs_waybill
```

### View Logs

```bash
# Application logs
sudo tail -f ${LOG_DIR}/gunicorn.log  # or uwsgi.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
sudo systemctl restart bhs_waybill
sudo systemctl restart nginx
```

## 9. Updating the Application

When you need to update your application:

```bash
cd /var/www/bhs_waybill
# Pull new code or copy new files
sudo git pull  # If using Git

# Update dependencies if needed
sudo venv/bin/pip install -r requirements.txt

# Regenerate configuration files if needed
sudo /var/www/bhs_waybill/venv/bin/python /var/www/bhs_waybill/deploy/generate_configs.py

# Restart the service
sudo systemctl restart bhs_waybill
```

## Troubleshooting

### Common Issues

1. **Permission Problems**:
   ```bash
   sudo chown -R www-data:www-data /var/www/bhs_waybill
   sudo chmod -R 755 /var/www/bhs_waybill
   ```

2. **Service Won't Start**:
   ```bash
   sudo journalctl -u bhs_waybill.service
   ```

3. **Nginx 502 Bad Gateway**:
   - Check if WSGI server is running
   - Verify socket permissions
   - Check logs for errors

4. **Static Files Not Loading**:
   - Verify paths in Nginx configuration
   - Check file permissions

5. **Environment Variables Not Applied**:
   - Make sure the `.env` file has the correct permissions
   - Regenerate configuration files
   - Restart the service
