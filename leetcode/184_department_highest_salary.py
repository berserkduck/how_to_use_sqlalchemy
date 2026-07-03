"""
https://leetcode.cn/problems/department-highest-salary/description/

表： Employee

+--------------+---------+
| 列名          | 类型    |
+--------------+---------+
| id           | int     |
| name         | varchar |
| salary       | int     |
| departmentId | int     |
+--------------+---------+
在 SQL 中，id是此表的主键。
departmentId 是 Department 表中 id 的外键（在 Pandas 中称为 join key）。
此表的每一行都表示员工的 id、姓名和工资。它还包含他们所在部门的 id。



表： Department

+-------------+---------+
| 列名         | 类型    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
在 SQL 中，id 是此表的主键列。
此表的每一行都表示一个部门的 id 及其名称。



查找出每个部门中薪资最高的员工。
按 任意顺序 返回结果表。
查询结果格式如下例所示。



示例 1:

输入：
Employee 表:
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 70000  | 1            |
| 2  | Jim   | 90000  | 1            |
| 3  | Henry | 80000  | 2            |
| 4  | Sam   | 60000  | 2            |
| 5  | Max   | 90000  | 1            |
+----+-------+--------+--------------+
Department 表:
+----+-------+
| id | name  |
+----+-------+
| 1  | IT    |
| 2  | Sales |
+----+-------+
输出：
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Jim      | 90000  |
| Sales      | Henry    | 80000  |
| IT         | Max      | 90000  |
+------------+----------+--------+
解释：Max 和 Jim 在 IT 部门的工资都是最高的，Henry 在销售部的工资最高。

"""

from sqlalchemy import (
    String,
    Integer,
    select,
    text,
    func,
    ChunkedIteratorResult,
)
from sqlalchemy.orm import Session, Mapped, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result, insert_data_and_commit


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    salary: Mapped[int] = mapped_column(Integer)
    departmentId: Mapped[int] = mapped_column(Integer)


class Department(Base):
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))


Base.metadata.create_all(engine)


class Solution:
    def sql(self, session: Session) -> ChunkedIteratorResult:
        sql = """
            with t as(
                select
                    d.name as department,
                    e.name as employee,
                    e.salary as salary,
                    dense_rank() over(partition by d.id order by salary desc) as rn
                from employee as e left join department as d
                on e.departmentId = d.id
            )
            select 
                department,
                employee,
                salary
            from t
            where rn = 1
        """
        result = session.execute(text(sql))
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        rn = (
            func.dense_rank()
            .over(partition_by=Department.id, order_by=Employee.salary.desc())
            .label("rn")
        )

        subquery = (
            select(
                Department.name.label("department"),
                Employee.name.label("employee"),
                Employee.salary.label("salary"),
                rn,
            )
            .select_from(Employee)
            .outerjoin(Department, Employee.departmentId == Department.id)
        ).alias("t")

        stmt = select(
            subquery.c.department, subquery.c.employee, subquery.c.salary
        ).where(subquery.c.rn == 1)

        result = session.execute(stmt)
        return result


if __name__ == "__main__":
    with Session(engine) as session:
        employees = [
            {"name": "Joe", "salary": "70000", "departmentId": 1},
            {"name": "Jim", "salary": "90000", "departmentId": 1},
            {"name": "Henry", "salary": "80000", "departmentId": 2},
            {"name": "Sam", "salary": "60000", "departmentId": 2},
            {"name": "Max", "salary": "90000", "departmentId": 1},
        ]

        departments = [{"name": "IT"}, {"name": "Sales"}]

        insert_data_and_commit(employees, Employee, session)
        insert_data_and_commit(departments, Department, session)

        print_tabulate_formatted_result(result=Solution().orm(session))
