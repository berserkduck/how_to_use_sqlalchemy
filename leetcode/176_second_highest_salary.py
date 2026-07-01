"""
https://leetcode.cn/problems/second-highest-salary/description/

Employee 表：

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| salary      | int  |
+-------------+------+
id 是这个表的主键。
表的每一行包含员工的工资信息。



查询并返回 Employee 表中第二高的 不同 薪水 。如果不存在第二高的薪水，查询应该返回 null(Pandas 则返回 None) 。

查询结果如下例所示。



示例 1：

输入：
Employee 表：
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
输出：
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+

示例 2：

输入：
Employee 表：
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
+----+--------+
输出：
+---------------------+
| SecondHighestSalary |
+---------------------+
| null                |
+---------------------+


"""

from sqlalchemy import Integer, select, text, ChunkedIteratorResult
from sqlalchemy.orm import Session, Mapped, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    salary: Mapped[int] = mapped_column(Integer)


Base.metadata.create_all(engine)


class Solution:
    def sql(self, session: Session) -> ChunkedIteratorResult:
        result = session.execute(
            text(
                "select (select distinct salary from employee order by salary desc limit 1 offset 1) as SecondHighestSalary"
            )
        )
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        subquery = (
            select(Employee.salary)
            .distinct()
            .order_by(Employee.salary.desc())
            .offset(1)
            .limit(1)
            .scalar_subquery()
        )

        result = session.execute(
            select(subquery.label("SecondHighestSalary"))
        )
        return result

if __name__ == "__main__":
    with Session(engine) as session:
        employees = [
            {"salary":100},
            {"salary":200},
            {"salary":300},
        ]
        
        for i in range(len(employees)):
            employee = Employee(**employees[i])
            session.add(employee)

        session.commit()

        print_tabulate_formatted_result(result=Solution().orm(session))