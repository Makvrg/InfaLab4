from typing import List, Dict, Tuple, Union, Any

from main.deserializer.Token import Token
from main.deserializer.YAMLTokenizer import YAMLTokenizer


class YAMLDeserializer:

    @staticmethod
    def __deserialize_sequence(tokens: List[Token]) -> Tuple[List, int]:
        output_list: List = []
        count_tokens: int = 0

        while count_tokens < len(tokens):
            current_token: Token = tokens[count_tokens]
            if current_token.type == "BLOCK_END":
                count_tokens += 1
                return output_list, count_tokens
            elif current_token.type == "SCALAR":
                count_tokens += 1
                output_list.append(current_token.value)
            elif current_token.type == "BLOCK_SEQUENCE_START":
                count_tokens += 1
                value: List
                step: int
                value, step = (
                    YAMLDeserializer.__deserialize_sequence(tokens[count_tokens:])
                )
                count_tokens += step
                output_list.append(value)
            elif current_token.type == "BLOCK_MAPPING_START":
                count_tokens += 1
                value: Dict
                step: int
                value, step = (
                    YAMLDeserializer.__deserialize_mapping(tokens[count_tokens:])
                )
                count_tokens += step
                output_list.append(value)
            else:
                raise ValueError(
                    f"Неожиданный токен с type={current_token.type}, "
                    + f"value={current_token.value}"
                )

    @staticmethod
    def __deserialize_mapping(tokens: List[Token]) -> Tuple[Dict, int]:
        output_dict: Dict = dict()
        count_tokens: int = 0

        while count_tokens < len(tokens):
            current_token: Token = tokens[count_tokens]
            if current_token.type == "BLOCK_END":
                count_tokens += 1
                return output_dict, count_tokens
            elif current_token.type == "KEY":
                if count_tokens + 1 < len(tokens):

                    count_tokens += 1
                    key: str = current_token.value
                    value: Union[str, List, Dict]
                    step: int
                    next_token: Token = tokens[count_tokens]

                    if next_token.type == "SCALAR":
                        value: str = next_token.value
                        step = 1
                    elif next_token.type == "BLOCK_SEQUENCE_START":
                        count_tokens += 1
                        value, step = (YAMLDeserializer
                                       .__deserialize_sequence(tokens[count_tokens:]))
                    elif next_token.type == "BLOCK_MAPPING_START":
                        count_tokens += 1
                        value, step = (YAMLDeserializer
                                       .__deserialize_mapping(tokens[count_tokens:]))
                    else:
                        raise ValueError(
                            f"Неожиданный токен после KEY с type={next_token.type}, "
                            + f"value={next_token.value}"
                        )
                    output_dict[key] = value
                    count_tokens += step

                else:
                    raise ValueError(f"Получен некорректный список токенов: {tokens}")
            else:
                raise ValueError(
                    f"Неожиданный токен с type={current_token.type}, "
                    + f"value={current_token.value}"
                )

    @staticmethod
    def deserialize(yaml_text: str) -> Tuple[Any, List[str]]:
        tokens, comments = YAMLTokenizer.tokenize(yaml_text)

        if tokens[0].type == "SCALAR":
            if isinstance(tokens[0].value, str):
                python_object = str(tokens[0].value)
            elif isinstance(tokens[0].value, bool):
                python_object = tokens[0].value
            elif tokens[0].value is None:
                python_object = None
            if len(tokens) != 1:
                raise ValueError(f"Неверная структура данных: {yaml_text}")
        elif tokens[0].type == "BLOCK_SEQUENCE_START":
            python_object, step = (
                YAMLDeserializer.__deserialize_sequence(tokens[1:])
            )
        elif tokens[0].type == "BLOCK_MAPPING_START":
            python_object, step = (
                YAMLDeserializer.__deserialize_mapping(tokens[1:])
            )
        else:
            raise ValueError(f"Неверная структура данных: {yaml_text}")

        return python_object, comments
