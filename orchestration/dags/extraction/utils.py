import yaml


def read_yaml_file(path: str) -> dict:
    with open(path) as stream:
        try:
            data: dict = yaml.safe_load(stream)

            return data
        except yaml.YAMLError as err:
            raise yaml.YAMLError(f"Error while trying to read {path}: {err}") from err
