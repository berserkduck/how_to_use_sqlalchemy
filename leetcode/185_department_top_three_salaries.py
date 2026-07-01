"""
https://leetcode.cn/problems/department-top-three-salaries/description/

表: Employee

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| id           | int     |
| name         | varchar |
| salary       | int     |
| departmentId | int     |
+--------------+---------+
id 是该表的主键列(具有唯一值的列)。
departmentId 是 Department 表中 ID 的外键（reference 列）。
该表的每一行都表示员工的ID、姓名和工资。它还包含了他们部门的ID。



表: Department

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
id 是该表的主键列(具有唯一值的列)。
该表的每一行表示部门ID和部门名。



公司的主管们感兴趣的是公司每个部门中谁赚的钱最多。一个部门的 高收入者 是指一个员工的工资在该部门的 不同 工资中 排名前三 。

编写解决方案，找出每个部门中 收入高的员工 。

以 任意顺序 返回结果表。

返回结果格式如下所示。



示例 1:

输入:
Employee 表:
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 85000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
| 7  | Will  | 70000  | 1            |
+----+-------+--------+--------------+
Department  表:
+----+-------+
| id | name  |
+----+-------+
| 1  | IT    |
| 2  | Sales |
+----+-------+
输出:
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| IT         | Joe      | 85000  |
| IT         | Randy    | 85000  |
| IT         | Will     | 70000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |
+------------+----------+--------+
解释:
在IT部门:
- Max的工资最高
- 兰迪和乔都赚取第二高的独特的薪水
- 威尔的薪水是第三高的

在销售部:
- 亨利的工资最高
- 山姆的薪水第二高
- 没有第三高的工资，因为只有两名员工



提示：

    没有姓名、薪资和部门 完全 相同的员工。


"""

from sqlalchemy import String, Integer, select, text, func, ChunkedIteratorResult
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
                    salary,
                    dense_rank() over(partition by departmentid order by salary desc) rn
                from employee e join department d on e.departmentid = d.id
            )
            select
                department,
                employee,
                salary
            from t
            where rn <=3
        """
        result = session.execute(text(sql))
        return result

    def orm(self, session: Session) -> ChunkedIteratorResult:
        # 排序字段
        rn = func.dense_rank().over(
            partition_by=Employee.departmentId, order_by=Employee.salary.desc()
        )

        """
         这种解法使用内连接或左连接都可以，这里使用内连接。
         SQLAlchemy 使用 join() 实现内连接
         join()中的目标表影响 SQL 中表的出现顺序：
            join(Employee) -> department join employee
            join(Department) -> employee join department
        """
        subquery = (
            select(
                Department.name.label("department"),
                Employee.name.label("employee"),
                Employee.salary,
                rn.label("rn"),
            )
            .join(Employee, Employee.departmentId == Department.id)
            .alias("t")
        )
        stmt = select(
            subquery.c.department, subquery.c.employee, subquery.c.salary
        ).where(subquery.c.rn <= 3)
        result = session.execute(stmt)
        return result

if __name__ == "__main__":
    with Session(engine) as session:
        employees = [
            {"name": "Joe", "salary": "85000", "departmentId": 1},
            {"name": "Henry", "salary": "80000", "departmentId": 2},
            {"name": "Sam", "salary": "60000", "departmentId": 2},
            {"name": "Max", "salary": "90000", "departmentId": 1},
            {"name": "Janet", "salary": "69000", "departmentId": 1},
            {"name": "Randy", "salary": "85000", "departmentId": 1},
            {"name": "Will", "salary": "70000", "departmentId": 1},
        ]

        departments = [{"name": "IT"}, {"name": "Sales"}]

        insert_data_and_commit(employees, Employee, session)
        insert_data_and_commit(departments, Department, session)

        print_tabulate_formatted_result(result=Solution().orm(session))
