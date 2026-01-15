"""
SubHunterX Pro - Helper Utilities
"""
import os
import yaml
from pathlib import Path


def load_config():
    """Load configuration from YAML or create default"""
    config_path = "config/config.yaml"
    
    # Default config
    default_config = {
        'subhunterx': {
            'threads': 50,
            'timeout': 8,
            'rate_limit': 0.1,
            'screenshot': False,
            'max_screenshots': 20
        },
        'database': {
            'path': './subhunterx_pro.db'
        },
        'wordlists': {
            'brute_size': 1000
        },
        'api': {
            'host': '127.0.0.1',
            'port': 8000
        }
    }
    
    # Try to load from file
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                loaded_config = yaml.safe_load(f)
                if loaded_config:
                    # Merge with defaults
                    for key in default_config:
                        if key in loaded_config:
                            default_config[key].update(loaded_config[key])
        except Exception as e:
            print(f"⚠️  Error loading config: {e}, using defaults")
    else:
        # Create config directory and file
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        try:
            with open(config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
        except Exception as e:
            print(f"⚠️  Could not create config file: {e}")
    
    return default_config


def color_status(status_code):
    """Return colored status code for terminal display"""
    if status_code is None:
        return "[dim]N/A[/dim]"
    
    status_code = int(status_code)
    
    if 200 <= status_code < 300:
        return f"[green]{status_code}[/green]"
    elif 300 <= status_code < 400:
        return f"[yellow]{status_code}[/yellow]"
    elif 400 <= status_code < 500:
        return f"[orange]{status_code}[/orange]"
    elif 500 <= status_code < 600:
        return f"[red]{status_code}[/red]"
    else:
        return f"[dim]{status_code}[/dim]"


def sanitize_filename(filename):
    """Sanitize filename for safe file operations"""
    import re
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    return filename


def format_size(bytes_size):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def extract_domain(url):
    """Extract domain from URL"""
    import re
    # Remove protocol
    domain = re.sub(r'^https?://', '', url)
    # Remove path
    domain = domain.split('/')[0]
    # Remove port
    domain = domain.split(':')[0]
    return domain


def is_valid_domain(domain):
    """Check if domain is valid"""
    import re
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))


def create_directory_structure():
    """Create necessary directories for SubHunterX"""
    directories = [
        'data/screenshots',
        'data/wordlists',
        'reports',
        'config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    return True
