import os


def env(name):
    try:
        return os.environ[name]
    except KeyError:
        raise KeyError(f"Значення змінної оточення {name} не задано")
