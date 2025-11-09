from types import NoneType
from typing import List, Dict, Tuple


class XMLSerializer:

    @staticmethod
    def __serialize_mapping(inner_map: Dict, indent: int = 0) -> str:
        return XMLSerializer.__serialize_with_key_value(inner_map.items(),
                                                        indent)

    @staticmethod
    def __serialize_sequence(inner_seq: List, indent: int = 0) -> str:
        enum_seq: List[Tuple] = [
            (f"row-{index}", element) for index, element in enumerate(inner_seq)
        ]
        return XMLSerializer.__serialize_with_key_value(enum_seq,
                                                        indent)

    @staticmethod
    def __serialize_with_key_value(pairs, indent: int):
        inner_xml_text: str = ""
        for key, value in pairs:

            inner_xml_text += " " * indent + f"<{key}>"

            if type(value) in [bool, NoneType, str]:
                if value is True:
                    inner_xml_text += f"true</{key}>\n"
                elif value is False:
                    inner_xml_text += f"false</{key}>\n"
                elif value is None:
                    inner_xml_text += f"</{key}>\n"
                else:
                    inner_xml_text += f"{value}</{key}>\n"
            elif isinstance(value, dict):
                inner_xml_text += "\n" + XMLSerializer.__serialize_mapping(value,
                                                                           indent + 2)
                inner_xml_text += " " * indent + f"</{key}>\n"
            elif isinstance(value, list):
                inner_xml_text += "\n" + XMLSerializer.__serialize_sequence(value,
                                                                            indent + 2)
                inner_xml_text += " " * indent + f"</{key}>\n"
            else:
                raise ValueError(
                    f"Получен некорректный тип бинарного внутреннего объекта: {type(value)}"
                )

        return inner_xml_text


    @staticmethod
    def serialize(python_object, comments: List[str] = []):
        xml_text: str = ""

        for comment in comments:
            xml_text += f"<!-- {comment} -->\n"

        if python_object is True:
            xml_text += f"<row-0>true/<row-0>\n"
        elif python_object is False:
            xml_text += f"<row-0>false</row-0>\n"
        elif python_object is None:
            xml_text += f"<row-0></row-0>\n"
        elif isinstance(python_object, str):
            xml_text += f"<row-0>{python_object}</row-0>\n"

        elif type(python_object) == dict:
            xml_text += XMLSerializer.__serialize_mapping(python_object)
        elif type(python_object) == list:
            xml_text += XMLSerializer.__serialize_sequence(python_object)
        else:
            raise ValueError(
                f"Получен некорректный тип бинарного внешнего объекта: {type(python_object)}"
            )

        return xml_text
