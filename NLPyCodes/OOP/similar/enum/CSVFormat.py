from enum import Enum
class CSVFormat(Enum):
    V1 = 1
    """
    CSV 내부 DataFrame이 \\n\\n 문자열로 분리되어있는 포맷에 경우 사용
    """
    V2 = 2
    """
    CSV가 DataFrame이 아닌 단순 구분 문자열이며 헤더, 디버깅용 테이블이 제거된 경량화 포맷인 경우 사용
    """