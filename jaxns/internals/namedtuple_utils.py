import importlib

import numpy as np


def isinstance_namedtuple(obj) -> bool:
    """
    Check if object is a namedtuple.

    Args:
        obj: object

    Returns:
        bool
    """
    return (
            isinstance(obj, tuple) and
            hasattr(obj, '_asdict') and
            hasattr(obj, '_fields')
    )


def issubclass_namedtuple(cls):
    """
    Check if the type object is a subclass of a namedtuple.
    """
    base_types = cls.__mro__  # Get the method resolution order of the class
    return any(hasattr(base, '_fields') and hasattr(base, '_asdict') for base in base_types)


def serialise_namedtuple(obj):
    if isinstance_namedtuple(obj):
        class_name = f"{obj.__class__.__module__}.{obj.__class__.__name__}"
        return {'type': '__namedtuple__', '__class__': class_name,
                '__data__': {k: serialise_namedtuple(v) for k, v in obj._asdict().items()}}
    elif isinstance(obj, np.ndarray):
        return serialise_ndarray(obj)
    elif isinstance(obj, (list, tuple)):
        return [serialise_namedtuple(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: serialise_namedtuple(v) for k, v in obj.items()}
    else:
        return obj


def deserialise_namedtuple(obj):
    if isinstance(obj, dict) and 'type' in obj and obj['type'] == '__namedtuple__':
        class_path = obj['__class__']
        module_name, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        return class_(**{k: deserialise_namedtuple(v) for k, v in obj['__data__'].items()})
    elif isinstance(obj, dict) and 'type' in obj and obj['type'] == '__ndarray__':
        return deserialise_ndarray(obj)
    elif isinstance(obj, (list, tuple)):
        return [deserialise_namedtuple(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: deserialise_namedtuple(v) for k, v in obj.items()}
    return obj


def serialise_ndarray(obj):
    if isinstance(obj, np.ndarray):
        return {'type': '__ndarray__', '__dtype__': str(obj.dtype), '__data__': obj.tolist()}
    return obj


def deserialise_ndarray(obj):
    if isinstance(obj, dict) and obj.get('type') == '__ndarray__':
        return np.array(obj['__data__'], dtype=obj['__dtype__'])
    return obj
