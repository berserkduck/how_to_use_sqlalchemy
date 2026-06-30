"""
https://leetcode.cn/problems/employees-earning-more-than-their-managers/description/

表：Employee

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| salary      | int     |
| managerId   | int     |
+-------------+---------+
id 是该表的主键（具有唯一值的列）。
该表的每一行都表示雇员的ID、姓名、工资和经理的ID。



编写解决方案，找出收入比经理高的员工。

以 任意顺序 返回结果表。

结果格式如下所示。



示例 1:

输入:
Employee 表:
+----+-------+--------+-----------+
| id | name  | salary | managerId |
+----+-------+--------+-----------+
| 1  | Joe   | 70000  | 3         |
| 2  | Henry | 80000  | 4         |
| 3  | Sam   | 60000  | Null      |
| 4  | Max   | 90000  | Null      |
+----+-------+--------+-----------+
输出:
+----------+
| Employee |
+----------+
| Joe      |
+----------+
解释: Joe 是唯一挣得比经理多的雇员。

"""

from sqlalchemy import String, Integer, text, select, alias, ChunkedIteratorResult
from sqlalchemy.orm import Session, Mapped, mapped_column
from db import Base, engine
from utils import print_tabulate_formatted_result

class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    salary: Mapped[int] = mapped_column(Integer)
    managerId: Mapped[int] = mapped_column(Integer, nullable=True)


Base.metadata.create_all(engine)

class Solution:
    def sql(self, session: Session) -> ChunkedIteratorResult:
        result = session.execute(
            text(
                "select e1.name as employee from employee as e1 left join employee as e2 on e1.managerId = e2.id where e1.salary > e2.salary"
            )
        )
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        # 使用 alias 给表或子查询起别名
        employee = alias(Employee, name="e1") # 等价于 SQL employee as e1
        manager = alias(Employee, name="e2") # 等价于 SQL employee as e2

        stmt = (
            # 使用 label 给查询结果中的列起别名
            # employee.c.name 中的 c 是 column collection（列集合）
            # alias(Employee, name="e1") 生成了一个带别名的表对象，通过 employee.c 访问这个别名表上列
            select(employee.c.name.label("employee"))
            .select_from(employee)
            .outerjoin(manager, employee.c.managerId == manager.c.id)
            .where(employee.c.salary > manager.c.salary)
        )

        result = session.execute(stmt)
        return result

if __name__ == "__main__":
    with Session(engine) as session:

        employees = [
            {"name": "Joe", "salary": "70000", "managerId": 3},
            {"name": "Henry", "salary": "80000", "managerId": 4},
            {"name": "Sam", "salary": "60000", "managerId": None},
            {"name": "Max", "salary": "90000", "managerId": None},
        ]

        for i in range(len(employees)):
            employee = Employee(**employees[i])
            session.add(employee)

        session.commit()

        print_tabulate_formatted_result(result=Solution.orm(session)) 


