import yaml


class YAMLDeserializerWithLib:

    @staticmethod
    def deserialize(yaml_text: str):
        python_object = yaml.safe_load(yaml_text)
        return python_object
