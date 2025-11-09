from typing import List, Tuple

from main.deserializer.Token import Token
from main.deserializer.YAMLLineHandler import YAMLLineHandler


class YAMLTokenizer:

    @staticmethod
    def tokenize(yaml_text: str) -> Tuple[List[Token], List[str]]:
        tokens: List[Token] = []
        indent_stack: List[int] = [0]
        block_stack: List[str] = []

        lines, comments = YAMLLineHandler.cut_comments(yaml_text)

        for line in lines:

            striped: str = line.strip()
            escaped_sequence_line = YAMLLineHandler.escape_sequence(striped)
            indent = len(line) - len(line.lstrip(" "))

            # Закрытие блоков при уменьшении отступа
            while indent < indent_stack[-1]:
                indent_stack.pop()
                tokens.append(Token("BLOCK_END"))
                if block_stack:
                    block_stack.pop()

            # Список
            if escaped_sequence_line.startswith("- ") or escaped_sequence_line == "-":
                if (not block_stack or block_stack[-1] != "sequence"
                    or (indent > indent_stack[-1] and block_stack[-1] == "sequence")):
                    tokens.append(Token("BLOCK_SEQUENCE_START"))
                    block_stack.append("sequence")
                    indent_stack.append(indent)

                escaped_sequence_line = escaped_sequence_line[1:].strip()

                if ":" in escaped_sequence_line:
                    key, _, val = escaped_sequence_line.partition(":")
                    tokens.append(Token("BLOCK_MAPPING_START"))
                    block_stack.append("mapping")
                    indent_stack.append(indent + 2)
                    tokens.append(
                        Token("KEY",
                              YAMLLineHandler
                              .replace_special_sequence(key.strip()))
                    )
                    if val.strip():
                        tokens.append(
                            Token("SCALAR",
                                  YAMLLineHandler
                                  .replace_special_sequence(val.strip()))
                        )
                elif escaped_sequence_line:
                    tokens.append(
                        Token("SCALAR",
                              YAMLLineHandler
                              .replace_special_sequence(escaped_sequence_line))
                    )

            # Словарь
            elif ":" in escaped_sequence_line:
                if (not block_stack or block_stack[-1] != "mapping"
                        or (block_stack[-1] == "mapping" and indent_stack[-1] != indent)):
                    tokens.append(Token("BLOCK_MAPPING_START"))
                    block_stack.append("mapping")
                    indent_stack.append(indent)

                key, _, val = escaped_sequence_line.partition(":")
                tokens.append(
                    Token("KEY",
                          YAMLLineHandler
                          .replace_special_sequence(key.strip()))
                )
                if val.strip():
                    tokens.append(
                        Token("SCALAR",
                              YAMLLineHandler
                              .replace_special_sequence(val.strip()))
                    )

            # Вся введённая структура является скаляром или неверна
            else:
                if len(lines) == 1:
                    tokens.append(
                        Token("SCALAR",
                              YAMLLineHandler
                              .replace_special_sequence(line.strip()))
                    )
                    return tokens, comments
                else:
                    raise ValueError(f"Неверная введённая структура: {yaml_text}")

        # Закрытие всех оставшихся блоков
        while block_stack:
            block_stack.pop()
            tokens.append(Token("BLOCK_END"))

        return tokens, comments
