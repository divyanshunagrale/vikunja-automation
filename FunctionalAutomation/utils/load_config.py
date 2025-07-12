import os
import yaml

def load_config():
    # print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    # print(os.path.dirname(__file__))
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config = os.path.join(root, 'config.yaml')
    with open(config, 'r') as f:
        return yaml.safe_load(f)