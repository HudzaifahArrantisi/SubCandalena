"""
SubHunterX Pro Configuration Module
"""
import os
import yaml

def load_config():
    """Load configuration from YAML or create default"""
    config_path = "config/config.yaml"
    
    # Default config
    default_config = {
        'subhunterx': {
            'threads': 50,  # Reduced untuk testing
            'timeout': 8,
            'rate_limit': 0.1,
            'screenshot': False,  # Disabled untuk testing
            'max_screenshots': 20
        },
        'database': {
            'path': './subhunterx_pro.db'
        },
        'wordlists': {
            'brute_size': 1000  # Reduced untuk testing
        },
        'api': {
            'host': '127.0.0.1',
            'port': 8000
        }
    }
    
    # Create config dir & default file if not exists
    os.makedirs('config', exist_ok=True)
    
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        print(f"✅ Created default config: {config_path}")
    
    # Load config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Merge defaults
    for section, defaults in default_config.items():
        if section not in config:
            config[section] = {}
        config[section].update(defaults.get(section, {}))
    
    return config