import configparser
from io import StringIO
from typing import Dict, List, Any


class INISerializerWithLib:

    @staticmethod
    def __serialize_mapping(inner_map: Dict, root: str = "") -> Dict[str, str]:
        return INISerializerWithLib.__serialize_with_key_value(inner_map.items(),
                                                               root)

    @staticmethod
    def __serialize_sequence(inner_seq: List, root: str = "") -> Dict[str, str]:
        return INISerializerWithLib.__serialize_with_key_value(enumerate(inner_seq),
                                                               root)

    @staticmethod
    def __serialize_with_key_value(pairs, root: str = "") -> Dict[str, str]:
        flat = {}
        for key, value in pairs:
            inner_root = f"{root}.{key}" if root else str(key)

            if isinstance(value, bool):
                flat[inner_root] = "true" if value else "false"
            elif value is None:
                flat[inner_root] = ""
            elif isinstance(value, str):
                flat[inner_root] = '"' + value + '"'
            elif isinstance(value, dict):
                flat.update(INISerializerWithLib.__serialize_with_key_value(value.items(),
                                                                            inner_root)
                            )
            elif isinstance(value, list):
                flat.update(INISerializerWithLib.__serialize_with_key_value(enumerate(value),
                                                                            inner_root)
                            )
            else:
                raise ValueError(
                    f"Получен некорректный тип бинарного внутреннего объекта: {type(value)}"
                )
        return flat


    @staticmethod
    def serialize(python_object: Any, comments: List[str] = []) -> str:
        cfg = configparser.ConfigParser()
        section_name: str = "serialized"
        cfg.add_section(section_name)

        if isinstance(python_object, dict):
            flat_dict = INISerializerWithLib.__serialize_mapping(python_object)
        elif isinstance(python_object, list):
            flat_dict = INISerializerWithLib.__serialize_sequence(python_object)
        elif isinstance(python_object, bool):
            flat_dict = {"0": "true" if python_object else "false"}
        elif python_object is None:
            flat_dict = {"0": ""}
        elif isinstance(python_object, str):
            flat_dict = {"0": python_object}
        else:
            raise ValueError(
                f"Получен некорректный тип бинарного внешнего объекта: {type(python_object)}"
            )

        for key, value in flat_dict.items():
            cfg.set(section_name, key, value)

        buf = StringIO()
        cfg.write(buf)

        ini_text = ""
        for comment in comments:
            ini_text += f"; {comment}\n"
        ini_text += buf.getvalue()
        return ini_text
