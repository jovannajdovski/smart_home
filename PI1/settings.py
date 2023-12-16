import json
import os
def load_settings(filePath='..\config\settings.json'):
    script_dir = os.path.dirname(__file__)
    
    # Create the absolute path to the settings.json file
    absolute_path = os.path.join(script_dir, filePath)
    
    with open(absolute_path, 'r') as f:
        return json.load(f)