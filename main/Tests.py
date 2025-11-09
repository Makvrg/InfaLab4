from main.deserializer.YAMLDeserializerWithLib import YAMLDeserializerWithLib
from main.serializer.INISerializer import INISerializer
from main.deserializer.YAMLDeserializer import YAMLDeserializer
from main.serializer.INISerializerWithLib import INISerializerWithLib

yaml_text1 = """
items:
  - name: Alice #1
    tags: # 2
      - 'pyt:hon'
      - 'go#'
    meta:
      active: YES   
      score: null
  - name: Bob
  # 3 comment
    tags: ~
    meta: ~
"""
yaml_text2 = """
american:
  - Boston Red Sox # Comment
  - Detroit Tigers
  - New York Yankees
national:
  - New York Mets
  - Chicago Cubs
  - Atlanta Braves
"""

#tokens: List[Token] = YAMLTokenizer.tokenize(yaml_text2)
#print("Count tokens:", len(tokens))
#for t in tokens:
#    print(t)

# python_object, comments = YAMLDeserializer.deserialize(yaml_text1)
# print(INISerializer.serialize(python_object, comments))

# python_object_lib = YAMLDeserializerWithLib.deserialize(yaml_text1)
# python_object_my, comments = YAMLDeserializer.deserialize(yaml_text1)
# print(python_object_lib == python_object_my)
# print("lib:", python_object_lib)
# print("my :", python_object_my)

data = {
    "database": {"driver": {"1": True, "2": "b"}, "host": "localhost", "active": True, "password": None},
    "user": {"name": "Alice", "role": "admin"}
}

print(INISerializer.serialize(data, ["ss", 'dkmd ']))
print()
ini_text = INISerializerWithLib.serialize(data, ["ss", "dkmd"])
print(ini_text)
