from typing import List, Any

import pytest

from main.serializer.INISerializerWithLib import INISerializerWithLib


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
american.0 = Boston Red Sox
american.1 = Detroit Tigers
american.2 = New York Yankees
national.0 = New York Mets
national.1 = Chicago Cubs
national.2 = Atlanta Braves
"""
         ),
        (
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
                },
                ["1", "2", "3 comment"],
"""; 1
; 2
; 3 comment
[serialized]
items.0.name = Alice
items.0.tags.0 = pyt:hon
items.0.tags.1 = go #
items.0.meta.active = true
items.0.meta.score = 
items.1.name = Bob
items.1.tags = 
items.1.meta = 
"""
         )
    ]
)
def test_ini_serializer_with_lib(python_object: Any,
                                 comments: List[str],
                                 expected_ini_text: str):
    ini_text: str = INISerializerWithLib.serialize(python_object, comments)
    assert ini_text == expected_ini_text
