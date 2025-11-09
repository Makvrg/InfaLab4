from typing import List, Dict, Union, Any

import pytest

from main.serializer.INISerializer import INISerializer


@pytest.mark.parametrize(
    "python_object, comments, expected_ini_text",
    [
        (
                {
                    "american": ["Boston Red Sox", "Detroit Tigers", "New York Yankees"],
                    "national": ["New York Mets", "Chicago Cubs", "Atlanta Braves"]
                },
                ["Comment 1", "Comment 2"],
"""; Comment 1
; Comment 2
[serialized]
american.0 = "Boston Red Sox"
american.1 = "Detroit Tigers"
american.2 = "New York Yankees"
national.0 = "New York Mets"
national.1 = "Chicago Cubs"
national.2 = "Atlanta Braves"
"""
         )
    ]
)
def test_serializer(python_object: Any,
                    comments: List[str],
                    expected_ini_text: str):
    ini_text: str = INISerializer.serialize(python_object, comments)
    assert ini_text == expected_ini_text
