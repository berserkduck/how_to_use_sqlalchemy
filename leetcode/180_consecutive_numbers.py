"""
https://leetcode.cn/problems/consecutive-numbers/description/

表：Logs

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
在 SQL 中，id 是该表的主键。
id 是一个自增列。



找出所有至少连续出现三次的数字。

返回的结果表中的数据可以按 任意顺序 排列。

结果格式如下面的例子所示：



示例 1:

输入：
Logs 表：
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+
输出：
Result 表：
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
解释：1 是唯一连续出现至少三次的数字。

"""

from sqlalchemy import Integer, select, text, func, ChunkedIteratorResult
from sqlalchemy.orm import Session, Mapped, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result


class Logs(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    num: Mapped[int] = mapped_column(Integer)


Base.metadata.create_all(engine)


class Solution:
    def sql(self, session: Session) -> ChunkedIteratorResult:
        result = session.execute(text("""
                select distinct num as consecutivenums
                from (
                    select
                        id,
                        num,
                        row_number() over(order by id) - row_number() over(partition by num order by id) as const_value
                    from logs
                    ) as t
                group by num, const_value
                having count(1) >=3
                """))
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        serial_number = func.row_number().over(order_by=Logs.id)
        serial_group_number = func.row_number().over(partition_by=Logs.num, order_by=Logs.id)
        const_value = serial_number - serial_group_number

        subquery = select(
            Logs.id.label("id"), Logs.num.label("num"), const_value.label("const_value")
        ).alias("t")

        stmt = (
            select(subquery.c.num.label("consecutivenums"))
            .group_by(subquery.c.num, subquery.c.const_value)
            .having(func.count(1) >= 3)
        )

        result = session.execute(stmt)

        return result


if __name__ == "__main__":
    with Session(engine) as session:

        logs = [1, 1, 1, 2, 1, 2, 2]

        for i in range(len(logs)):
            log = Logs(num=logs[i])
            session.add(log)

        session.commit()

        print_tabulate_formatted_result(result=Solution().orm(session))
