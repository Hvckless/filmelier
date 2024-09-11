from enum import Enum
class CSVFormat(Enum):
    V1 = 1
    """
    CSV 내부 DataFrame이 \\n\\n 문자열로 분리되어있는 포맷에 경우 사용
    """