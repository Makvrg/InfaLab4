from typing import List, Any

import pytest

from main.serializer.XMLSerializer import XMLSerializer


@pytest.mark.parametrize(
    "python_object, comments, expected_xml_text",
    [
        (
                {
                    "american": ["Boston Red Sox", "Detroit Tigers", "New York Yankees"],
                    "national": ["New York Mets", "Chicago Cubs", "Atlanta Braves"]
                },
                ["Comment 1", "Comment 2"],
"""<!-- Comment 1 -->
<!-- Comment 2 -->
<american>
  <row-0>Boston Red Sox</row-0>
  <row-1>Detroit Tigers</row-1>
  <row-2>New York Yankees</row-2>
</american>
<national>
  <row-0>New York Mets</row-0>
  <row-1>Chicago Cubs</row-1>
  <row-2>Atlanta Braves</row-2>
</national>
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
"""<!-- 1 -->
<!-- 2 -->
<!-- 3 comment -->
<items>
  <row-0>
    <name>Alice</name>
    <tags>
      <row-0>pyt:hon</row-0>
      <row-1>go #</row-1>
    </tags>
    <meta>
      <active>true</active>
      <score></score>
    </meta>
  </row-0>
  <row-1>
    <name>Bob</name>
    <tags></tags>
    <meta></meta>
  </row-1>
</items>
"""
         )
    ]
)
def test_xml_serializer(python_object: Any,
                        comments: List[str],
                        expected_xml_text: str):
    xml_text: str = XMLSerializer.serialize(python_object, comments)
    assert xml_text == expected_xml_text
