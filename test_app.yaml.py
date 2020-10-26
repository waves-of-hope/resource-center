import yaml
from decouple import config, Csv

with open('app.yaml', 'r') as file:
    settings = yaml.full_load(file)

if __name__ == "__main__":
    for key, value in settings['env_variables'].items():
        print(key, ":", value)