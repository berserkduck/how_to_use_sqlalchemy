from tabulate import tabulate
from sqlalchemy.engine.result import ChunkedIteratorResult


def print_tabulate_formatted_result(result: ChunkedIteratorResult, format: str = "grid") -> None:
    """
    使用 tabulate 打印查询结果

    args:
        result: sqlalchemy 查询结果的 result 对象
        format: tabulate 表格输出格式
    """
    rows = []

    for row in result.mappings():
        row_data = [value if value is not None else "Null" for value in row.values()]
        rows.append(row_data)

    headers = result.keys()

    table = tabulate(rows, headers=headers, tablefmt=format)

    print(table)
