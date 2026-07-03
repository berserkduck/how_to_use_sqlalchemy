"""
https://leetcode.cn/problems/rising-temperature/description/

表： Weather

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| recordDate    | date    |
| temperature   | int     |
+---------------+---------+
id 是该表具有唯一值的列。
没有具有相同 recordDate 的不同行。
该表包含特定日期的温度信息



编写解决方案，找出与之前（昨天的）日期相比温度更高的所有日期的 id 。

返回结果 无顺序要求 。

结果格式如下例子所示。



示例 1：

输入：
Weather 表：
+----+------------+-------------+
| id | recordDate | Temperature |
+----+------------+-------------+
| 1  | 2015-01-01 | 10          |
| 2  | 2015-01-02 | 25          |
| 3  | 2015-01-03 | 20          |
| 4  | 2015-01-04 | 30          |
+----+------------+-------------+
输出：
+----+
| id |
+----+
| 2  |
| 4  |
+----+
解释：
2015-01-02 的温度比前一天高（10 -> 25）
2015-01-04 的温度比前一天高（20 -> 30）

"""

from sqlalchemy import (
    String,
    Integer,
    select,
    text,
    func,
    ChunkedIteratorResult,
)
from sqlalchemy.orm import Session, Mapped, aliased, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result, insert_data_and_commit


class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(primary_key=True)
    recordDate: Mapped[str] = mapped_column(String(10))
    temperature: Mapped[int] = mapped_column(Integer)


Base.metadata.create_all(engine)


class Solution:
    def sql(self, session: Session) -> ChunkedIteratorResult:
        """
        SQLite 自连接解法

        weather表自连接：
        - w1：“今天的温度”
        - w2：“昨天的温度”
        通过连接条件限定日期差为1天

        SQLite 不支持 datediff、date_add、date_sub 函数

        SQLite 的日期处理函数date(): date(时间值, '修饰符')

        date(日期, '+1 days') 等价于 date_add(日期, interval 1 day)
        """
        sql = """
            select w1.id
            from weather w1 join weather w2
            on w1.recordDate = date(w2.recordDate, '+1 days')
            where w1.temperature > w2.temperature
        """

        result = session.execute(text(sql))
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        w1 = aliased(Weather)
        w2 = aliased(Weather)

        # func 对象的用法 
        # 调用 func.date()、func.count()、func.dense_rank() 等时，这些方法并不真实存在于 SQLAlchemy 中
        # func.date() 被转为 func.__getattr__('date') ，动态创建一个表示 SQL date() 函数的对象
        # 执行查询时，SQLAlchemy 将其转为 SQL 中对应的函数
        stmt = (
            select(w1.id)
            .join(w2, w1.recordDate == func.date(w2.recordDate, "+1 days"))
            .where(
                w1.temperature > w2.temperature,
            )
        )
        result = session.execute(stmt)
        return result


if __name__ == "__main__":
    with Session(engine) as session:
        weather = [
            {"recordDate": "2015-01-01", "temperature": 10},
            {"recordDate": "2015-01-02", "temperature": 25},
            {"recordDate": "2015-01-03", "temperature": 20},
            {"recordDate": "2015-01-04", "temperature": 30},
        ]

        insert_data_and_commit(weather, Weather, session)
        print_tabulate_formatted_result(result=Solution().orm(session))
