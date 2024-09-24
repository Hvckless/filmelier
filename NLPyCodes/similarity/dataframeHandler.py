import pandas as pd
from io import StringIO
from typing import Dict

DataFrameList = list[pd.DataFrame]


#completed
def splitDataFrame22(filepath:str)->DataFrameList:
    """
    ⛔ 완성됨. 수정하기 전에 잘못된 함수를 수정하는 것이 아닌지 주의할 것. ⛔
    """


    content:str = "undefined"
    tables:DataFrameList = []


    with open(filepath, 'r', encoding="utf-8") as file:
        content = file.read()

    tables_content:list[str] = content.split('\n\n')

    for table_content in tables_content:
        tables.append(pd.read_csv(StringIO(table_content)))

    return tables