from typing import List

from yamlparser.Token import Token
from yamlparser.YAMLDeserializer import YAMLDeserializer
from yamlparser.YAMLTokenizer import YAMLTokenizer

yaml_text1 = """
items:
  - name: Alice
    tags:
      - 'pyt:hon'
      - 'go'
    meta:
      active: true
      score: null
  - name: Bob
    tags: ~
    meta: ~
"""
yaml_text2 = """
canonical: 1.23015e+3
exponential: 12.3015e+02
fixed: 1230.15
negative infinity: -.inf
not a number: .NaN
"""

tokens: List[Token] = YAMLTokenizer.tokenize(yaml_text2)
print("Count tokens:", len(tokens))
#for t in tokens:
#    print(t)

python_object = YAMLDeserializer.deserialize(yaml_text2)
print(python_object)
