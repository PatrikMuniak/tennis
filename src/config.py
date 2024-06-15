import yaml

venue_config=None
with open('config.yaml', 'r') as file:
    venue_config = yaml.safe_load(file)