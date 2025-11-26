from typing import Any

import pytest

from main.deserializer.YAMLDeserializerWithLib import YAMLDeserializerWithLib


@pytest.mark.parametrize(
    "yaml_text, expected_python_object",
    [
        (
"""american:
  - Boston Red Sox # Comment 1
  - Detroit Tigers
  - New York Yankees
national: # Comment 2
  - New York Mets
  - Chicago Cubs
  - Atlanta Braves""",
                {
                    "american": ["Boston Red Sox", "Detroit Tigers", "New York Yankees"],
                    "national": ["New York Mets", "Chicago Cubs", "Atlanta Braves"]
                }
        ),
        (
"""
items:
  - name: Alice #1
    tags: # 2
      - 'pyt:hon'
      - 'go #'
    meta:
      active: YES
      score: null
  - name: Bob
  # 3 comment
    tags: ~
    meta: Null""",
                {
                    "items": [
                        {
                            "name": "Alice",
                            "tags": ["pyt:hon", "go #"],
                            "meta": {"active": True, "score": None}
                        },
                        {
                            "name": "Bob",
                            "tags": None,
                            "meta": None
                        }
                    ]
                }
        )
    ]
)
def test_yaml_deserializer_with_lib(yaml_text: str,
                                    expected_python_object: Any):
    python_object = YAMLDeserializerWithLib.deserialize(yaml_text)
    assert python_object == expected_python_object
