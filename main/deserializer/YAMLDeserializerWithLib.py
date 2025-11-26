from typing import Any

import yaml


class YAMLDeserializerWithLib:

    @staticmethod
    def deserialize(yaml_text: str) -> Any:
        python_object = yaml.safe_load(yaml_text)
        return python_object
