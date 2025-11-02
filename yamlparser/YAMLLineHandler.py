from typing import List


class YAMLLineHandler:

    @staticmethod
    def clean_comments(yaml_text: str) -> List[str]:
        lines: List[str] = yaml_text.splitlines()

        output_lines: List[str] = []

        for line in lines:
            if not line.strip() or line.strip().startswith("#"):
                continue

            escaped_sequence_line = YAMLLineHandler.escape_sequence(line)
            if "#" in escaped_sequence_line:
                index_hashtag: int = escaped_sequence_line.find("#")
                escaped_sequence_line = escaped_sequence_line[:index_hashtag]

            output_lines.append(escaped_sequence_line)

        return output_lines

    @staticmethod
    def escape_sequence(line: str) -> str:
        minor_line: str = line
        indexes: List[int] = [-1]
        while "'" in minor_line[indexes[-1] + 1:]:
            indexes.append(minor_line.index("'", indexes[-1] + 1))
        del indexes[0]
        if len(indexes) > 1:
            output_line: str = ""
            count_pairs: int = len(indexes) // 2
            for i in range(0, count_pairs * 2, 2):
                substring: str = minor_line[indexes[i] + 1:indexes[i + 1]]
                while (":" in substring or "-" in substring
                       or "~" in substring or "#" in substring):
                    substring = substring.replace(":", "|*_tWoPoInT_*|")
                    substring = substring.replace("-", "|*_sHoRtLiNe_*|")
                    substring = substring.replace("~", "|*_tIlDa_*|")
                    substring = substring.replace("#", "|*_hAsHtAg_*|")

                if i == 0:
                    start_index: int = 0
                else:
                    start_index: int = indexes[i - 1] + 1

                output_line += (minor_line[start_index:indexes[i]]
                                + "|*_sTaRtSeQ_*|" + substring + "|*_eNdSeQ_*|")
            output_line += minor_line[indexes[count_pairs * 2 - 1] + 1:]
        else:
            output_line: str = minor_line

        return output_line

    @staticmethod
    def replace_special_sequence(val: str):
        if val == "~":
            return None
        while ("|*_tWoPoInT_*|" in val or "|*_sHoRtLiNe_*|" in val
               or "|*_tIlDa_*|" in val or "|*_sTaRtSeQ_*|" in val
               or "|*_eNdSeQ_*|" in val or "|*_hAsHtAg_*|" in val):
            val = val.replace("|*_tWoPoInT_*|", ":")
            val = val.replace("|*_sHoRtLiNe_*|", "-")
            val = val.replace("|*_tIlDa_*|", "~")
            val = val.replace("|*_hAsHtAg_*|", "#")
            val = val.replace("|*_sTaRtSeQ_*|", "")
            val = val.replace("|*_eNdSeQ_*|", "")
        return val
