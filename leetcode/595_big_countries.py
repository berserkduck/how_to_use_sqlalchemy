"""
https://leetcode.cn/problems/big-countries/description/

World 表：

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| name        | varchar |
| continent   | varchar |
| area        | int     |
| population  | int     |
| gdp         | bigint  |
+-------------+---------+
name 是该表的主键（具有唯一值的列）。
这张表的每一行提供：国家名称、所属大陆、面积、人口和 GDP 值。



如果一个国家满足下述两个条件之一，则认为该国是 大国 ：

    面积至少为 300 万平方公里（即，3000000 km2），或者
    人口至少为 2500 万（即 25000000）

编写解决方案找出 大国 的国家名称、人口和面积。

按 任意顺序 返回结果表。

返回结果格式如下例所示。



示例：

输入：
World 表：
+-------------+-----------+---------+------------+--------------+
| name        | continent | area    | population | gdp          |
+-------------+-----------+---------+------------+--------------+
| Afghanistan | Asia      | 652230  | 25500100   | 20343000000  |
| Albania     | Europe    | 28748   | 2831741    | 12960000000  |
| Algeria     | Africa    | 2381741 | 37100000   | 188681000000 |
| Andorra     | Europe    | 468     | 78115      | 3712000000   |
| Angola      | Africa    | 1246700 | 20609294   | 100990000000 |
+-------------+-----------+---------+------------+--------------+
输出：
+-------------+------------+---------+
| name        | population | area    |
+-------------+------------+---------+
| Afghanistan | 25500100   | 652230  |
| Algeria     | 37100000   | 2381741 |
+-------------+------------+---------+


"""

from sqlalchemy import String, Integer, select,text, or_, ChunkedIteratorResult
from sqlalchemy.orm import Session, Mapped, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result


class World(Base):
    __tablename__ = "world"

    name: Mapped[str] = mapped_column(String(255), primary_key=True)
    continent: Mapped[str] = mapped_column(String(255))
    area: Mapped[int] = mapped_column(Integer)
    population: Mapped[int] = mapped_column(Integer)
    gdp: Mapped[int] = mapped_column(Integer)


Base.metadata.create_all(engine)


class Solution:

    def sql(self, session: Session) -> ChunkedIteratorResult:
        result = session.execute(
            text(
                "select name, population, area from world where area >= 3000000 or population >= 25000000"
            )
        )
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        # stmt = select(World.name, World.population, World.area).where((World.area >= 3000000) | (World.population >= 25000000))
        stmt = select(World.name, World.population, World.area).where(
            or_(World.area >= 3000000, World.population >= 25000000)
        )
        result = session.execute(stmt)
        return result


if __name__ == "__main__":
    with Session(engine) as session:

        countries = [
            {
                "name": "Afghanistan",
                "continent": "Asia",
                "area": 652230,
                "population": 25500100,
                "gdp": 20343000000,
            },
            {
                "name": "Albania",
                "continent": "Europe",
                "area": 28748,
                "population": 2831741,
                "gdp": 12960000000,
            },
            {
                "name": "Algeria",
                "continent": "Africa",
                "area": 2381741,
                "population": 37100000,
                "gdp": 188681000000,
            },
            {
                "name": "Andorra",
                "continent": "Europe",
                "area": 468,
                "population": 78115,
                "gdp": 3712000000,
            },
            {
                "name": "Angola",
                "continent": "Africa",
                "area": 1246700,
                "population": 20609294,
                "gdp": 100990000000,
            },
        ]

        for i in range(len(countries)):
            country = World(**countries[i])
            session.add(country)

        session.commit()

        print_tabulate_formatted_result(result=Solution().orm(session))
