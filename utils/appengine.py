import os
from google.cloud import datastore as cloud_datastore

from . import datastore

DATASTORE_KIND = 'Application Configuration'


class AppEngineConfig(object):

    def __init__(self, kind=DATASTORE_KIND, debug=False):
        """Defines properties for the class

        Args:
            kind (str, optional): Used to categorize entities in datastore.
                Defaults to DATASTORE_KIND.
        """
        # Instantiates a cloud datastore client
        self.client = cloud_datastore.Client()
        self.debug = debug

        # The environment that the app will run in
        #  e.g: staging, test, production
        self.environment = os.getenv('APP_SERVICE', 'default')
        self.kind = kind
        self.name = self.environment + '-service-config'

    def __str__(self):
        """Returns a string representation of the object

        Returns:
            str: A string representing an object
        """
        return 'App Engine configuration for {} environment'.format(
            self.environment
        )

    def create(self, config_vars=None):
        """Creates config variables for an environment

        Args:
            config_vars (dict, optional): The config variables you want to set.
                Defaults to None.

        Returns:
            dict_items: A dictionary-like data structure containing
                the config variables
        """
        # create the config
        entity = datastore.create_entity(
            self.client, self.kind, self.name, config_vars
        )
        # get the config vars from the created entity
        config_vars = entity.items()

        if self.debug:
            print('Created the following config variables for the {} environment:'.\
                format(self.environment)
            )
            print(str(config_vars) + '\n')
        return config_vars

    def retrieve(self):
        """Retrieves config variables for an environment

        Returns:
            dict_items: A dictionary-like data structure containing
                the config variables
        """
        # retrieve the config
        entity = datastore.retrieve_entity(
            self.client, self.kind, self.name
        )
        # get the config vars from the retrieved entity
        try:
            config_vars = entity.items()
        except AttributeError:
            return None

        if self.debug:
            print('Retrieved the following config variables for the {} environment:'.\
                format(self.environment)
            )
            print(str(config_vars) + '\n')
        return config_vars

    def update(self, config_vars=None):
        """Updates config variables for an environment

        Returns:
            dict_items: A dictionary-like data structure containing
                the config variables
        """
        # update the config
        entity = datastore.create_entity(
            self.client, self.kind, self.name, config_vars
        )
        # get the config vars from the updated entity
        config_vars = entity.items()

        if self.debug:
            print('Updated the following config variables for the {} environment:'.\
                format(self.environment)
            )
            print(str(config_vars) + '\n')
        return config_vars

    def delete(self):
        """Deletes config variables for an environment
        """
        # delete the config
        datastore.retrieve_entity(self.client, self.kind, self.name)

        if self.debug:
            print('Deleted all config variables for the {} environment'.\
                format(self.environment)
            )

    def set_environment_variables_from_config(self):
        """Sets environment variables from an environment config
        """
        # retrieve the config
        env_vars = self.retrieve()
    
        # set env vars from the config
        if env_vars:
            for key, value in env_vars:
                os.environ[key] = value


if __name__ == '__main__':
    config_vars = {
        'DJANGO_SECRET_KEY': os.getenv('DJANGO_SECRET_KEY', ''),
        'DJANGO_DEBUG': True,
    }

    updated_config_vars = {
        'DJANGO_DEBUG': os.getenv('DJANGO_DEBUG', False),
        'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS', ''),
    }
    debug = True
    os.environ['APP_SERVICE'] = 'test'

    test_env_config = AppEngineConfig(debug=debug)
    test_env_config.create(config_vars)
    test_env_config.retrieve()
    test_env_config.update(updated_config_vars)

    os.environ['DJANGO_DEBUG'] = 'True'
    test_env_config.set_environment_variables_from_config()
    assert os.getenv('DJANGO_DEBUG') == 'False'

    test_env_config.delete()
