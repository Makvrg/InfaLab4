from typing import Tuple, Any, List

from main.deserializer.YAMLDeserializer import YAMLDeserializer
from main.deserializer.YAMLDeserializerWithLib import YAMLDeserializerWithLib

from main.serializer.INISerializer import INISerializer
from main.serializer.INISerializerWithLib import INISerializerWithLib

from main.serializer.XMLSerializer import XMLSerializer


class Lab:

    @staticmethod
    def deserialize(yaml_text: str) -> Tuple[Any, List[str]]:
        return YAMLDeserializer.deserialize(yaml_text)

    @staticmethod
    def deserialize_with_lib(yaml_text: str) -> Any:
        return YAMLDeserializerWithLib.deserialize(yaml_text)

    @staticmethod
    def serialize_to_ini(python_object: Any, comments: List[str]) -> str:
        return INISerializer.serialize(python_object, comments)

    @staticmethod
    def serialize_to_ini_with_lib(python_object: Any, comments: List[str]) -> str:
        return INISerializerWithLib.serialize(python_object, comments)

    @staticmethod
    def serialize_to_xml(python_object: Any, comments: List[str]) -> str:
        return XMLSerializer.serialize(python_object, comments)


if __name__ == "__main__":
    yaml_timetable: str = ""

    with open(file="resourses/YAMLtimetable", encoding="utf-8") as yaml_file:
        yaml_timetable = yaml_file.read()

    python_obj, comments = Lab.deserialize(yaml_timetable)
    python_object_from_lib: str = Lab.deserialize_with_lib(yaml_timetable)

    ini_text = Lab.serialize_to_ini(python_obj, comments)
    ini_text_from_lib: str = Lab.serialize_to_ini_with_lib(python_object_from_lib, comments)

    xml_text: str = Lab.serialize_to_xml(python_obj, comments)
    xml_text_from_lib_text: str = Lab.serialize_to_xml(python_object_from_lib, comments)

    print(xml_text)

