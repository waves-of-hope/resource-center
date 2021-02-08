from datetime import datetime, timedelta

from google.cloud import datastore


def create_entity(client, kind, name, properties, debug=False):
    """Creates a cloud datastore entity

    Args:
        client (object): A cloud datastore client
        kind (string): The kind for the new entity
        name (string): The name/ID for the new entity
        properties (dict): A dictionary containing the properties
            of the entity

    Returns:
        object: A cloud datastore entity
    """
    # The Cloud Datastore key for the new entity
    entity_key = client.key(kind, name)

    # Prepares the new entity
    entity = datastore.Entity(key=entity_key)
    if properties:
        for key, value in properties.items():
            entity[key] = value

    # Saves the entity
    client.put(entity)
    if debug:
        print(f"Created entity: {entity}")

    return entity

def retrieve_entity(client, kind, name, debug=False):
    """Retrieves a cloud datastore entity

    Args:
        client (object): A cloud datastore client
        kind (string): The kind for the new entity
        name (string): The name/ID for the new entity

    Returns:
        object: A cloud datastore entity
    """
    # create the key from kind and name
    entity_key = client.key(kind, name)

    # retrieve the entity
    entity = client.get(entity_key)
    if debug:
        print(f"Retrieved entity: {entity}")

    return entity

def update_entity(client, kind, name, properties, debug=False):
    """Updates a cloud datastore entity

    Args:
        client (object): A cloud datastore client
        kind (string): The kind for the new entity
        name (string): The name/ID for the new entity
        properties (dict): A dictionary containing the properties
            of the entity

    Returns:
        object: A cloud datastore entity
    """
    with client.transaction():
        # retrieve the entity
        entity = retrieve_entity(client=client, kind=kind, name=name)

        # update properties if they exist
        if properties:
            for key, value in properties.items():
                entity[key] = value

        client.put(entity)
        if debug:
            print(f"Updated entity: {entity}")

    return entity

def delete_entity(client, kind, name, debug=False):
    """Deletes a cloud datastore entity

    Args:
        client (object): A cloud datastore client
        kind (string): The kind for the new entity
        name (string): The name/ID for the new entity
    """
    entity_key = client.key(kind, name)
    client.delete(entity_key)
    if debug:
        print(f"Deleted entity: ({kind}, {name})")


if __name__ == '__main__':
    # Instantiates a client
    datastore_client = datastore.Client()
    kind = 'Task'
    name = 'sampletask1'
    properties = {'description': 'Write tests for this module'}
    updated_properties = {
        'description': 'Finish writing tests for this module',
        'deadline': datetime.now() + timedelta(minutes=30)
    }
    debug = True

    entity = create_entity(datastore_client, kind, name, properties, debug)
    entity = retrieve_entity(datastore_client, kind, name, debug)
    entity = update_entity(datastore_client, kind, name, updated_properties, debug)

    print(f'Entity Key: {entity.key}')
    print(f'Entity Properties: {entity.items()}')

    delete_entity(datastore_client, kind, name, debug)
