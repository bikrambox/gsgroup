#!/usr/bin/env python3
"""
Script to generate configuration files from templates using environment variables.
This script should be run on the deployment server to create the actual configuration files.
"""

import os
import sys
from string import Template
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent
DEPLOY_DIR = BASE_DIR / 'deploy'

# Define the configuration templates and their output paths
CONFIG_FILES = {
    'nginx.conf': '/etc/nginx/sites-available/bhs_waybill',
    'uwsgi.ini': BASE_DIR / 'uwsgi.ini',
    'uwsgi.service': '/etc/systemd/system/bhs_waybill.service',
    'gunicorn.service': '/etc/systemd/system/bhs_waybill.service',
    'supervisor.conf': '/etc/supervisor/conf.d/bhs_waybill.conf'
}

# Add additional environment variables that might be needed
os.environ.setdefault('APP_PATH', str(BASE_DIR))
os.environ.setdefault('VENV_PATH', str(BASE_DIR / 'venv'))

def generate_config_file(template_path, output_path):
    """Generate a configuration file from a template using environment variables."""
    try:
        # Read the template file
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Create a template object
        template = Template(template_content)
        
        # Substitute environment variables
        output_content = template.safe_substitute(os.environ)
        
        # Create the output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Write the output file
        with open(output_path, 'w') as f:
            f.write(output_content)
        
        print(f"Generated {output_path}")
        return True
    except Exception as e:
        print(f"Error generating {output_path}: {e}", file=sys.stderr)
        return False

def main():
    """Main function to generate all configuration files."""
    success = True
    
    for template_name, output_path in CONFIG_FILES.items():
        template_path = DEPLOY_DIR / template_name
        
        # Check if the template file exists
        if not template_path.exists():
            print(f"Template file {template_path} does not exist", file=sys.stderr)
            success = False
            continue
        
        # Generate the configuration file
        if not generate_config_file(template_path, output_path):
            success = False
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
