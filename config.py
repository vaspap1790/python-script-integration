import json

with open('config.json') as f:
    config = json.load(f)

# You need to add the following keys to a config.json file:
PD_API_TOKEN = config.get('PD_API_TOKEN')
ABSOLUTE_PROJECT_PATH = config.get('PROJECT_STACK_CONFIG_DIR')