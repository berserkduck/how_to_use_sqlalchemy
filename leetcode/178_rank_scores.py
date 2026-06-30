"""
https://leetcode.cn/problems/rank-scores/description/

表: Scores

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| score       | decimal |
+-------------+---------+
id 是该表的主键（有不同值的列）。
该表的每一行都包含了一场比赛的分数。Score 是一个有两位小数点的浮点值。



编写一个解决方案来查询分数的排名。排名按以下规则计算:

    分数应按从高到低排列。
    如果两个分数相等，那么两个分数的排名应该相同。
    在排名相同的分数后，排名数应该是下一个连续的整数。换句话说，排名之间不应该有空缺的数字。

按 score 降序返回结果表。

查询结果格式如下所示。



示例 1:

输入:
Scores 表:
+----+-------+
| id | score |
+----+-------+
| 1  | 3.50  |
| 2  | 3.65  |
| 3  | 4.00  |
| 4  | 3.85  |
| 5  | 4.00  |
| 6  | 3.65  |
+----+-------+
输出:
+-------+------+
| score | rank |
+-------+------+
| 4.00  | 1    |
| 4.00  | 1    |
| 3.85  | 2    |
| 3.65  | 3    |
| 3.65  | 3    |
| 3.50  | 4    |
+-------+------+
"""

from sqlalchemy import Double, select, text, func, ChunkedIteratorResult
from sqlalchemy.orm import Session, Mapped, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result


class Scores(Base):
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[float] = mapped_column(Double)


Base.metadata.create_all(engine)


class Solution:
    def sql(self, session: Session) -> ChunkedIteratorResult:
        result = session.execute(
            text(
                "select scores.score, dense_rank() over (order by score desc ) as 'rank' from scores order by score desc"
            )
        )
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        stmt = select(
            Scores.score,
            func.dense_rank().over(order_by=Scores.score.desc()).label("rank"),
        ).order_by(Scores.score.desc())
        result = session.execute(stmt)
        return result

if __name__ == "__main__":
    with Session(engine) as session:

        scores = [
            {"score": 3.5},
            {"score": 3.65},
            {"score": 4.0},
            {"score": 3.85},
            {"score": 4.0},
            {"score": 3.65},
        ]

        for i in range(len(scores)):
            score = Scores(**scores[i])
            session.add(score)

        session.commit()

        print_tabulate_formatted_result(result=Solution.orm(session))
