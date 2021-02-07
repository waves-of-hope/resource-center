def list_of_tuples(str):
    tuples = [tuple(tpl.split(':')) for tpl in str.split(',')]
    return tuples
