import importlib
import os


def load_models(path: str) -> list:
    """
    This method used to load models from given path

    Arguments:
        path {str} -- [The path that contains models]
    """
    dir_name = os.path.basename(path)
    packages = os.listdir(f"{path}/models")

    for package in packages:
        if str(package).endswith(".py") and str(package) != "__init__.py":
            package = str(package).replace(".py", "")
            module_name = f"{dir_name}.models.{package}"
            importlib.import_module(module_name)
