from types import NoneType
from typing import List, Dict, Any


class INISerializer:

    @staticmethod
    def __serialize_mapping(inner_map: Dict, root: str = "") -> str:
        return INISerializer.__serialize_with_key_value(inner_map.items(),
                                                        root)

    @staticmethod
    def __serialize_sequence(inner_seq: List, root: str = "") -> str:
        return INISerializer.__serialize_with_key_value(enumerate(inner_seq),
                                                        root)

    @staticmethod
    def __serialize_with_key_value(pairs, root: str):
        inner_ini_text: str = ""
        for key, value in pairs:

            inner_root = f"{root}.{key}" if root else str(key)

            if type(value) in [bool, NoneType, str]:
                if value is True:
                    inner_ini_text += f'{inner_root} = true\n'
                elif value is False:
                    inner_ini_text += f'{inner_root} = false\n'
                elif value is None:
                    inner_ini_text += f'{inner_root} = \n'
                else:
                    inner_ini_text += f'{inner_root} = {value}\n'
            elif isinstance(value, dict):
                inner_ini_text += INISerializer.__serialize_mapping(value,
                                                                    inner_root)
            elif isinstance(value, list):
                inner_ini_text += INISerializer.__serialize_sequence(value,
                                                                     inner_root)
            else:
                raise ValueError(
                    f"Получен некорректный тип бинарного внутреннего объекта: {type(value)}"
                )

        return inner_ini_text


    @staticmethod
    def serialize(python_object: Any, comments: List[str] = []) -> str:
        ini_text: str = ""

        for comment in comments:
            ini_text += f"; {comment}\n"

        ini_text += "[serialized]\n"

        if python_object is True:
            ini_text += f'0 = true\n'
        elif python_object is False:
            ini_text += f'0 = false\n'
        elif python_object is None:
            ini_text += f'0 = \n'
        elif isinstance(python_object, str):
            ini_text += f'0 = {python_object}\n'

        elif type(python_object) == dict:
            ini_text += INISerializer.__serialize_mapping(python_object)
        elif type(python_object) == list:
            ini_text += INISerializer.__serialize_sequence(python_object)
        else:
            raise ValueError(
                f"Получен некорректный тип бинарного внешнего объекта: {type(python_object)}"
            )

        return ini_text
