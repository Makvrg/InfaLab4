from typing import List, Dict, Union, Any

import pytest

from main.deserializer.YAMLDeserializer import YAMLDeserializer


@pytest.mark.parametrize(
    "yaml_text, expected_python_object, expected_comments",
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
                },
                ["Comment 1", "Comment 2"]
        )
    ]
)
def test_deserializer(yaml_text: str,
                      expected_python_object: Any,
                      expected_comments: List[str]):
    python_object, comments = YAMLDeserializer.deserialize(yaml_text)
    assert python_object == expected_python_object and comments == expected_comments
